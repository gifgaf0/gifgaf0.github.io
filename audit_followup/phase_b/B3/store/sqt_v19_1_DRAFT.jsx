import { useState, useEffect } from "react";

// ══════════════════════════════════════════════════════════════
//  SQT v1.9.1 DRAFT (October 2026) · CONSTANTS: one anchor (m_e), one selected scale (ξ_vac = 100φ)
//  and per-particle selections (knot, A, Z_f, L). A leading-order fit, not a zero-parameter derivation (ledger §2.92).
// ══════════════════════════════════════════════════════════════
const phi    = (1 + Math.sqrt(5)) / 2;
const phi2   = phi * phi;
const phi4   = phi2 * phi2;
const K0     = -phi2;        // Gaussian throat curvature K(0) = −φ², negative definite
const TWO_PI = 2 * Math.PI;
const PHI    = TWO_PI + K0 / (8 * Math.PI * Math.PI);
const m0     = 0.511 / Math.exp(TWO_PI / PHI);
const kappa  = 1 / phi4;
const XI_VAC = 100 * phi;   // selected scale; no combinatorial address (ledger §2.64.A)
const L_q    = PHI * phi2;  // Canonical companion ropelength Φφ² ≈ 16.363 fm (distinct from Up L=16.372)

function rEff(L) { return 1 + Math.log(1 + L / XI_VAC); }
function mass(A, Zf, L) {
  if (L === 0) return m0 * (A / Zf);
  const re = rEff(L);
  return m0 * (A / Zf) * Math.exp(L / (PHI * re));
}
function pct(pred, obs) { return (pred - obs) / obs * 100; }
function formatZf(zf) {
  if (Math.abs(zf - 0.75)          < 1e-6)  return "3/4";
  if (Math.abs(zf - 1/(8*phi4))    < 1e-9)  return "1/(8φ⁴)";
  if (Math.abs(zf - 1/(2*Math.PI)) < 1e-10) return "1/2π";
  if (zf < 1) return `1/${Math.round(1/zf)}`;
  return String(zf);
}
function fmtMeV(v) {
  if (Math.abs(v) >= 1e6) return `${(v/1e6).toFixed(3)} TeV`;
  if (Math.abs(v) >= 1e3) return `${(v/1e3).toFixed(4)} GeV`;
  if (Math.abs(v) < 0.001) return `${(v*1e6).toFixed(4)} eV`;
  return `${v.toFixed(4)} MeV`;
}

const ZF_LEPTON = 1 / (2 * Math.PI);
// obs: PDG 2024 (Navas et al., PRD 110, 030001): u, d, s M̄S at 2 GeV; c, b M̄S at their own scale; top direct.
// L: per-particle selected lengths, in mixed conventions. The quark values are ideal ropelengths per tube DIAMETER
// (trefoil 16.372 = 32.743 per radius; no nontrivial knot is below 31.32 per radius); L_e = 2π and the Borromean
// 58.006 are per RADIUS (audit B3, October 2026).
const PARTICLES = [
  { id:"up",      label:"Up",      type:"quark",  knot:"3₁",             A:3,   Zf:3,          L:16.372,   obs:2.16,    gen:"I",   col:"#22c55e" },
  { id:"down",    label:"Down",    type:"quark",  knot:"4₁",             A:11,  Zf:9,          L:21.04,    obs:4.70,    gen:"I",   col:"#22d3ee" },
  { id:"strange", label:"Strange", type:"quark",  knot:"6₁",             A:107, Zf:12,         L:29.13,    obs:93.5,    gen:"II",  col:"#f59e0b" },
  { id:"charm",   label:"Charm",   type:"quark",  knot:"5₁",             A:5,   Zf:1/48,       L:23.60,    obs:1273.0,  gen:"II",  col:"#f97316" },
  { id:"bottom",  label:"Bottom",  type:"quark",  knot:"8₁",             A:119, Zf:3/4,        L:37.31,    obs:4183,    gen:"III", col:"#a855f7" },
  { id:"top",     label:"Top",     type:"quark",  knot:"8₁⁹",            A:119, Zf:1/(8*phi4), L:37.31,    obs:172570,  gen:"III", col:"#ef4444" },
  { id:"electron",label:"Electron",type:"lepton", knot:"0₁",             A:1,   Zf:1,          L:TWO_PI,   obs:0.511,   gen:"I",   col:"#60a5fa" },
  { id:"muon",    label:"Muon",    type:"lepton", knot:"(2,1)-cable 0₁", A:1,   Zf:ZF_LEPTON,  L:2*L_q,    obs:105.658, gen:"II",  col:"#a78bfa" },
  { id:"tau",     label:"Tau",     type:"lepton", knot:"(3,1)-cable 3₁", A:3,   Zf:ZF_LEPTON,  L:3*L_q,    obs:1776.93, gen:"III", col:"#c084fc" },
];

// ── Fine-structure constants (Tab 16) ─────────────────────────
const ALPHA_OBS  = 137.035999;   // CODATA 2018
const ALPHA_BARE = 136.4789;     // α⁻¹ = 84/arctan(1/√2) — SQT bare coupling (Paper VII)
                                 // WHY 84? Conjecture: 84 = |PSL(2,7)|/2 = 168/2. Derivation pending.
const RP_EXACT   = 0.83847381;   // r_p for perfect α⁻¹ match at 8π
const RP_MUONIC  = 0.8414;       // muonic hydrogen 2013/2018 consensus
const RP_CODATA  = 0.8751;       // legacy electronic CODATA

function alphaInv(rp, solidAngle) {
  const fc = 1 + (rp * rp / solidAngle) * kappa;
  return ALPHA_BARE * fc;
}

const SOLID_ANGLES = [
  { label:"2π", val:2*Math.PI, desc:"Circle (1D winding)"       },
  { label:"4π", val:4*Math.PI, desc:"Sphere (3D surface)"       },
  { label:"8π", val:8*Math.PI, desc:"Double-cover spinor (SQT)" },
];
SOLID_ANGLES.forEach(sa => {
  let lo = 0.01, hi = 5.0;
  for (let i = 0; i < 60; i++) {
    const mid = (lo + hi) / 2;
    alphaInv(mid, sa.val) < ALPHA_OBS ? lo = mid : hi = mid;
  }
  sa.rp_req = (lo + hi) / 2;
  sa.physical = sa.rp_req > 0.80 && sa.rp_req < 0.92;
});

function buildAlphaCurve(N = 300) {
  const lo = 0.820, hi = 0.890;
  return Array.from({length:N}, (_, i) => {
    const rp = lo + (hi - lo) * i / (N - 1);
    return { rp, alpha: alphaInv(rp, 8 * Math.PI) };
  });
}

// ── Baryon constants (Tab 17 / Open Problem 5) ────────────────
const A_BORROMEAN  = 20;   // Σ coeff² of the diagonal Δ(t,t,t) = 1+9+9+1; the one-variable Alexander polynomial (t−1)⁴ gives 70
const ZF_BORROMEAN = 6;    // Conjecture 1 (|F₇*| = 6; F₇* ≅ Z₆ is not a subgroup of PSL(2,7), whose Fano-triangle stabilizer is S₃)
const L_B_BOUNDS   = { lo: 58.006, hi: 62.0 };  // lo: presumed-minimal tight Borromean rings (CFKSW 2006), an UPPER bound on the
                                                 // ideal ropelength, not a lower one; hi: no source, kept only for the slider scale

function borromeanL(m_target) {
  // Solve mass(A_BORROMEAN, ZF_BORROMEAN, L) = m_target by bisection
  let lo = 1, hi = 200;
  for (let i = 0; i < 80; i++) {
    const mid = (lo + hi) / 2;
    mass(A_BORROMEAN, ZF_BORROMEAN, mid) < m_target ? lo = mid : hi = mid;
  }
  return (lo + hi) / 2;
}
const L_B_PREDICTED = borromeanL(938.272);  // 60.194: m_p run backwards (an inversion, not a prediction; ledger §2.92)

// ── Colors ────────────────────────────────────────────────────
const BG   = "#07070f"; const PNL  = "#0d0d1a"; const BRD  = "#1a1a30";
const AMB  = "#f59e0b"; const GRN  = "#22c55e"; const RED  = "#ef4444";
const CYA  = "#22d3ee"; const PRP  = "#a855f7"; const ORG  = "#f97316";
const GRY  = "#6b7280"; const TXT  = "#e2e2e2"; const DIM  = "#111120";
const MONO = "'Courier New',monospace";

function errColor(e) {
  const a = Math.abs(e ?? 0);
  return a < 2 ? GRN : a < 8 ? AMB : a < 20 ? ORG : RED;
}
function Tag({ label, col }) {
  return <span style={{ fontFamily:MONO, fontSize:9, color:col, border:`1px solid ${col}`, borderRadius:2, padding:"1px 6px", letterSpacing:0.5, whiteSpace:"nowrap" }}>{label}</span>;
}
function SectionHead({ children, col }) {
  return <div style={{ fontFamily:MONO, fontSize:9, color:col||GRY, letterSpacing:3, marginBottom:12, marginTop:4, paddingBottom:6, borderBottom:`1px solid ${BRD}` }}>{children}</div>;
}
function Slider({ label, min, max, step, value, onChange, display, col }) {
  return (
    <div style={{ marginBottom:12 }}>
      <div style={{ display:"flex", justifyContent:"space-between", marginBottom:4 }}>
        <span style={{ fontSize:11, color:GRY }}>{label}</span>
        <span style={{ fontFamily:MONO, fontSize:12, color:col||TXT }}>{display ?? value}</span>
      </div>
      <input type="range" min={min} max={max} step={step} value={value}
        onChange={e => onChange(parseFloat(e.target.value))}
        style={{ width:"100%", accentColor:col||AMB, cursor:"pointer" }} />
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 1 — MASS AUDIT
// ══════════════════════════════════════════════════════════════
function MassAudit() {
  const [filter, setFilter] = useState("all");
  const rows = PARTICLES
    .filter(p => filter === "all" || p.type === filter)
    .map(p => ({ ...p, pred: mass(p.A, p.Zf, p.L), err: pct(mass(p.A, p.Zf, p.L), p.obs) }));

  return (
    <div>
      <SectionHead col={CYA}>THEOREM 1 · LOCAL MASS OPERATOR — LEADING-ORDER FIT AUDIT v1.9.1</SectionHead>
      <div style={{ background:"#0f0a00", border:`1px solid ${AMB}55`, borderLeft:`3px solid ${AMB}`, borderRadius:4, padding:"10px 14px", marginBottom:16, fontSize:11, color:GRY, lineHeight:1.7 }}>
        <span style={{ fontFamily:MONO, fontSize:9, color:AMB, letterSpacing:1 }}>STATUS · OCTOBER 2026 · </span>
        This table is a leading-order fit, not a set of predictions: one anchor (m_e), one selected scale (ξ_vac = 100φ) and
        per-particle selections (knot, A, Z_f, L). Observed values are PDG 2024; against them only b, t and τ fall within 2%.
        The electron row is the anchor (the formula returns 0.4925 MeV at L = 2π, the r_eff(2π) slack). Ledger §2.92.
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:10, marginBottom:20 }}>
        {[
          { label:"Φ (tension identity)",    val:PHI.toFixed(6),                    col:GRN },
          { label:"m₀ (energy anchor)",      val:`${m0.toFixed(5)} MeV`,            col:CYA },
          { label:"κ (bulk modulus)",        val:`1/φ⁴ ≈ ${kappa.toFixed(4)}`,      col:AMB },
          { label:"ξvac (correlation length)",val:`100φ ≈ ${XI_VAC.toFixed(2)}`,    col:PRP },
        ].map(s => (
          <div key={s.label} style={{ background:PNL, border:`1px solid ${BRD}`, borderTop:`2px solid ${s.col}`, borderRadius:4, padding:"10px 14px" }}>
            <div style={{ fontSize:9, color:GRY, fontFamily:MONO, letterSpacing:1, marginBottom:4 }}>{s.label}</div>
            <div style={{ fontFamily:MONO, fontSize:14, color:s.col }}>{s.val}</div>
          </div>
        ))}
      </div>
      <div style={{ display:"flex", gap:8, marginBottom:16 }}>
        {["all","quark","lepton"].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{ background:filter===f?PNL:"transparent", border:`1px solid ${filter===f?AMB:BRD}`, color:filter===f?AMB:GRY, padding:"4px 14px", borderRadius:3, fontFamily:MONO, fontSize:10, cursor:"pointer" }}>{f.toUpperCase()}</button>
        ))}
      </div>
      <div style={{ overflowX:"auto", marginBottom:20 }}>
        <table style={{ width:"100%", borderCollapse:"collapse", fontFamily:MONO, fontSize:11 }}>
          <thead>
            <tr style={{ borderBottom:`1px solid ${BRD}` }}>
              {["Gen","Particle","Knot","A","Zf","L","reff","Predicted","Observed","Error"].map(h => (
                <th key={h} style={{ padding:"7px 10px", textAlign:"left", fontSize:9, color:GRY, whiteSpace:"nowrap" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((p, i) => (
              <tr key={p.id} style={{ borderBottom:`1px solid ${DIM}`, background:i%2===0?"transparent":"#0d0d1a40" }}>
                <td style={{ padding:"7px 10px" }}><Tag label={`GEN ${p.gen}`} col={p.col}/></td>
                <td style={{ padding:"7px 10px", color:p.col, fontWeight:700 }}>{p.label}</td>
                <td style={{ padding:"7px 10px", color:GRY, fontSize:10 }}>{p.knot}</td>
                <td style={{ padding:"7px 10px", color:TXT }}>{p.A}</td>
                <td style={{ padding:"7px 10px", color:AMB }}>{formatZf(p.Zf)}</td>
                <td style={{ padding:"7px 10px", color:TXT }}>{p.L.toFixed(3)}</td>
                <td style={{ padding:"7px 10px", color:GRY }}>{rEff(p.L).toFixed(4)}</td>
                <td style={{ padding:"7px 10px", color:TXT }}>{fmtMeV(p.pred)}</td>
                <td style={{ padding:"7px 10px", color:GRY }}>{fmtMeV(p.obs)}</td>
                <td style={{ padding:"7px 10px" }}>
                  <span style={{ color:errColor(p.err), fontWeight:700 }}>{p.err>=0?"+":""}{p.err.toFixed(2)}%</span>
                  {(p.id==="up"||p.id==="muon") && <span style={{ fontSize:8, color:GRY, marginLeft:4 }}>[boundary]</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={{ background:DIM, border:`1px solid ${BRD}`, borderRadius:4, padding:"14px 18px" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>MASS FORMULA</div>
        <div style={{ fontFamily:MONO, fontSize:12, color:CYA, lineHeight:2.1 }}>
          m = m₀ · (A / Zf) · exp(L / (Φ · reff))
          <br/><span style={{ color:GRY }}>reff = 1 + ln(1 + L/ξvac) &nbsp;|&nbsp; Lepton Zf = 1/2π (v1.8) &nbsp;|&nbsp; Top Zf = 1/(8φ⁴)</span>
          <br/><span style={{ color:GRY }}>L: the quark values are per tube diameter; L_e = 2π and the Borromean 58.006 are per radius</span>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 2 — CALCULATOR
// ══════════════════════════════════════════════════════════════
function MassCalc() {
  const [L, setL]     = useState(16.372);
  const [A, setA]     = useState(3);
  const [Zf, setZf]   = useState(3);
  const [obs, setObs] = useState(2.2);

  const pred = mass(A, Zf, L);
  const re   = rEff(L);
  const err  = pct(pred, obs);
  const ec   = errColor(err);

  return (
    <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
      <div>
        <SectionHead col={AMB}>INPUTS</SectionHead>
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:4, padding:"16px 18px", marginBottom:14 }}>
          <Slider label="Ropelength L (fm)" min={TWO_PI} max={65} step={0.01} value={L} onChange={setL} display={`${L.toFixed(3)} fm`} col={CYA}/>
          <div style={{ fontSize:10, color:GRY, marginTop:-8, marginBottom:14 }}>
            ξvac = {XI_VAC.toFixed(2)} fm {L > PHI*PHI ? <span style={{ color:ORG }}> ⚠ approaching ropelength saturation (L_sat ≈ 39.06)</span> : ""}
          </div>
          <Slider label="Alexander Invariant A" min={1} max={200} step={1} value={A} onChange={setA} col={GRN}/>
          <div style={{ marginBottom:14 }}>
            <div style={{ fontSize:11, color:GRY, marginBottom:6 }}>Zf Stabilizer Phase</div>
            <div style={{ display:"flex", flexWrap:"wrap", gap:5, marginBottom:8 }}>
              {[
                { l:"1/(8φ⁴)",v:1/(8*phi4) },{ l:"1/48",v:1/48 },{ l:"1/2π",v:ZF_LEPTON },
                { l:"3/4",v:0.75 },{ l:"1",v:1 },{ l:"3",v:3 },{ l:"9",v:9 },{ l:"12",v:12 },
              ].map(o => (
                <button key={o.l} onClick={() => setZf(o.v)} style={{
                  background:Math.abs(Zf-o.v)<1e-9?PNL:"transparent",
                  border:`1px solid ${Math.abs(Zf-o.v)<1e-9?AMB:BRD}`,
                  color:Math.abs(Zf-o.v)<1e-9?AMB:GRY,
                  padding:"3px 9px", borderRadius:3, fontFamily:MONO, fontSize:9, cursor:"pointer"
                }}>{o.l}</button>
              ))}
            </div>
            <input type="number" value={Zf} step="0.0001" min="0.0001"
              onChange={e => setZf(Math.max(0.0001, parseFloat(e.target.value)||1))}
              style={{ background:"#0a0a18", border:`1px solid ${BRD}`, color:TXT, fontFamily:MONO, fontSize:11, padding:"4px 8px", borderRadius:3, width:"100%" }}/>
          </div>
          <div style={{ borderTop:`1px solid ${BRD}`, paddingTop:12 }}>
            <div style={{ fontSize:11, color:GRY, marginBottom:6 }}>Observed mass (MeV)</div>
            <input type="number" value={obs} step="0.01" min="0.001"
              onChange={e => setObs(Math.max(0.001, parseFloat(e.target.value)||1))}
              style={{ background:"#0a0a18", border:`1px solid ${BRD}`, color:TXT, fontFamily:MONO, fontSize:11, padding:"5px 10px", borderRadius:3, width:"100%" }}/>
          </div>
        </div>
        <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>QUICK PRESETS</div>
        <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:6 }}>
          {PARTICLES.map(p => (
            <button key={p.id} onClick={() => { setL(p.L); setA(p.A); setZf(p.Zf); setObs(p.obs); }}
              style={{ background:"transparent", border:`1px solid ${p.col}44`, color:p.col, padding:"5px 8px", borderRadius:3, fontFamily:MONO, fontSize:9, cursor:"pointer", textAlign:"left" }}>
              {p.label}
            </button>
          ))}
        </div>
      </div>
      <div>
        <SectionHead col={GRN}>CALCULATED OUTPUT</SectionHead>
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderTop:`2px solid ${ec}`, borderRadius:4, padding:"20px 22px", marginBottom:14 }}>
          <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>PREDICTED MASS</div>
          <div style={{ fontFamily:MONO, fontSize:36, color:ec, marginBottom:4 }}>{fmtMeV(pred)}</div>
          <div style={{ fontFamily:MONO, fontSize:12, color:GRY }}>Error: <span style={{ color:ec }}>{err>=0?"+":""}{err.toFixed(3)}%</span></div>
        </div>
        <div style={{ background:DIM, border:`1px solid ${BRD}`, borderRadius:4, padding:"14px 18px" }}>
          <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:10 }}>STEP-BY-STEP DERIVATION</div>
          {[
            { step:"reff",      val:`1 + ln(1+${L.toFixed(3)}/${XI_VAC.toFixed(2)}) = ${re.toFixed(6)}`,         col:AMB },
            { step:"Φ·reff",    val:`${PHI.toFixed(4)} × ${re.toFixed(4)} = ${(PHI*re).toFixed(6)}`,             col:AMB },
            { step:"exp(L/Φr)", val:`exp(${L.toFixed(3)}/${(PHI*re).toFixed(4)}) = ${Math.exp(L/(PHI*re)).toFixed(4)}`, col:ORG },
            { step:"A/Zf",      val:`${A} / ${formatZf(Zf)} = ${(A/Zf).toFixed(4)}`,                             col:PRP },
            { step:"mass",      val:`${m0.toFixed(5)} × ${(A/Zf).toFixed(4)} × ${Math.exp(L/(PHI*re)).toFixed(4)} = ${pred.toFixed(4)} MeV`, col:ec },
          ].map(row => (
            <div key={row.step} style={{ display:"grid", gridTemplateColumns:"80px 1fr", borderBottom:`1px solid #1a1a2e`, padding:"5px 0" }}>
              <span style={{ fontFamily:MONO, fontSize:10, color:GRY }}>{row.step}</span>
              <span style={{ fontFamily:MONO, fontSize:10, color:row.col }}>{row.val}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 3 — SPECTRUM
// ══════════════════════════════════════════════════════════════
function SpectrumChart() {
  const allP = PARTICLES.map(p => ({ ...p, pred:mass(p.A,p.Zf,p.L), logObs:Math.log10(p.obs) }));
  const minLog = -1; const maxLog = 6; const logSpan = maxLog - minLog;

  return (
    <div>
      <SectionHead col={GRN}>MASS SPECTRUM — LOG SCALE</SectionHead>
      <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:4, padding:"20px" }}>
        <div style={{ position:"relative", height:380 }}>
          {[-1,0,1,2,3,4,5,6].map(exp => {
            const frac = (exp-minLog)/logSpan;
            return (
              <div key={exp}>
                <div style={{ position:"absolute", right:"100%", top:`${(1-frac)*100}%`, transform:"translateY(-50%) translateX(-4px)", fontSize:9, color:GRY, fontFamily:MONO, whiteSpace:"nowrap" }}>10^{exp}</div>
                <div style={{ position:"absolute", left:0, right:0, top:`${(1-frac)*100}%`, height:1, background:DIM }}/>
              </div>
            );
          })}
          {allP.map((p, i) => {
            const x     = (i+0.5)/allP.length*100;
            const yObs  = (1-(p.logObs-minLog)/logSpan)*100;
            const lPred = Math.log10(Math.max(p.pred, 1e-10));
            const yPred = (1-(lPred-minLog)/logSpan)*100;
            const ec    = errColor(pct(p.pred,p.obs));
            return (
              <div key={p.id}>
                <div style={{ position:"absolute", left:`${x}%`, top:`${Math.min(yObs,yPred)}%`, width:2, height:`${Math.abs(yObs-yPred)}%`, background:`${ec}66`, transform:"translateX(-1px)" }}/>
                <div title={`${p.label} obs: ${fmtMeV(p.obs)}`} style={{ position:"absolute", left:`${x}%`, top:`${yObs}%`, width:10, height:10, borderRadius:"50%", background:p.col, border:`2px solid ${p.col}`, transform:"translate(-5px,-5px)", boxShadow:`0 0 6px ${p.col}88` }}/>
                <div title={`${p.label} pred: ${fmtMeV(p.pred)}`} style={{ position:"absolute", left:`${x}%`, top:`${yPred}%`, width:8, height:8, borderRadius:2, border:`2px solid ${ec}`, transform:"translate(-4px,-4px)" }}/>
                <div style={{ position:"absolute", left:`${x}%`, top:"calc(100% + 8px)", transform:"translateX(-50%) rotate(-40deg)", transformOrigin:"top left", fontSize:9, color:p.col, fontFamily:MONO, whiteSpace:"nowrap" }}>{p.label}</div>
              </div>
            );
          })}
        </div>
        <div style={{ display:"flex", gap:20, marginTop:52, paddingTop:10, borderTop:`1px solid ${BRD}`, justifyContent:"center", fontSize:10, color:GRY }}>
          <span>● Observed</span><span>□ Predicted</span>
          <span style={{ color:GRN }}>■ &lt;2%</span><span style={{ color:AMB }}>■ &lt;8%</span><span style={{ color:ORG }}>■ &lt;20%</span>
        </div>
      </div>
      <div style={{ marginTop:14, display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:8 }}>
        {allP.map(p => {
          const err = pct(p.pred,p.obs); const ec = errColor(err);
          return (
            <div key={p.id} style={{ background:PNL, border:`1px solid ${BRD}`, borderLeft:`3px solid ${ec}`, borderRadius:3, padding:"7px 12px" }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center" }}>
                <span style={{ fontSize:11, color:p.col }}>{p.label}</span>
                <span style={{ fontFamily:MONO, fontSize:12, color:ec }}>{err>=0?"+":""}{err.toFixed(2)}%</span>
              </div>
              <div style={{ height:2, background:DIM, borderRadius:1, marginTop:4 }}>
                <div style={{ width:`${Math.min(100,Math.abs(err)/20*100)}%`, height:"100%", background:ec, borderRadius:1 }}/>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 4 — WORTICITY
// ══════════════════════════════════════════════════════════════
function Worticity() {
  const PRESETS = [
    { label:"Up quarks only",    up:1e10, down:0,    charm:0, bottom:0, top:0 },
    { label:"Up + Down (paper)", up:1e10, down:1e10, charm:0, bottom:0, top:0 },
    { label:"Heavy remnants",    up:1e8,  down:1e8,  charm:1e6, bottom:1e5, top:1e3 },
  ];
  const [counts, setCounts] = useState({ up:1e10, down:1e10, charm:0, bottom:0, top:0 });
  const [Nprime, setNprime] = useState(5e9);
  const WEntry = [
    { id:"up",    A:3,   Zf:3,          col:GRN },
    { id:"down",  A:11,  Zf:9,          col:CYA },
    { id:"charm", A:5,   Zf:1/48,       col:ORG },
    { id:"bottom",A:119, Zf:0.75,       col:PRP },
    { id:"top",   A:119, Zf:1/(8*phi4), col:RED },
  ];
  const Wtotal    = WEntry.reduce((s,e) => s + (counts[e.id]||0)*e.A*e.Zf, 0);
  const WmaxLight = Nprime * 9;
  const needsHeavy = Wtotal > WmaxLight;
  function fmt(n) {
    if (n >= 1e12) return `${(n/1e12).toFixed(3)}×10¹²`;
    if (n >= 1e9)  return `${(n/1e9).toFixed(3)}×10⁹`;
    if (n >= 1e6)  return `${(n/1e6).toFixed(3)}×10⁶`;
    return n.toFixed(2);
  }
  return (
    <div>
      <SectionHead col={PRP}>THEOREM 2 · WORTICITY SUM RULE & AEON INHERITANCE</SectionHead>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
        <div>
          <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:10 }}>AEON N — DYING UNIVERSE COMPOSITION</div>
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:4, padding:"14px 16px", marginBottom:12 }}>
            {WEntry.map(e => (
              <div key={e.id} style={{ marginBottom:12 }}>
                <div style={{ display:"flex", justifyContent:"space-between", marginBottom:3 }}>
                  <span style={{ fontSize:11, color:e.col }}>{e.id.charAt(0).toUpperCase()+e.id.slice(1)} (A={e.A}, Zf={formatZf(e.Zf)})</span>
                  <span style={{ fontFamily:MONO, fontSize:11, color:TXT }}>W={(e.A*e.Zf).toFixed(4)}/particle</span>
                </div>
                <input type="range" min={0} max={1e11} step={1e8} value={counts[e.id]||0}
                  onChange={ev => setCounts(c => ({ ...c, [e.id]:parseFloat(ev.target.value) }))}
                  style={{ width:"100%", accentColor:e.col, cursor:"pointer" }}/>
                <div style={{ display:"flex", justifyContent:"space-between", fontSize:9, color:GRY }}>
                  <span>N = {fmt(counts[e.id]||0)}</span>
                  <span>W: {fmt((counts[e.id]||0)*e.A*e.Zf)}</span>
                </div>
              </div>
            ))}
          </div>
          <div style={{ display:"flex", gap:8, flexWrap:"wrap" }}>
            {PRESETS.map(p => (
              <button key={p.label} onClick={() => setCounts({ up:p.up, down:p.down, charm:p.charm, bottom:p.bottom, top:p.top })}
                style={{ background:"transparent", border:`1px solid ${BRD}`, color:GRY, padding:"4px 10px", borderRadius:3, fontFamily:MONO, fontSize:9, cursor:"pointer" }}>
                {p.label}
              </button>
            ))}
          </div>
        </div>
        <div>
          <div style={{ background:PNL, border:`1px solid ${PRP}`, borderTop:`2px solid ${PRP}`, borderRadius:4, padding:"16px 18px", marginBottom:12 }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, marginBottom:4 }}>Wtotal = Σ Aᵢ · Zf,ᵢ</div>
            <div style={{ fontFamily:MONO, fontSize:32, color:PRP, marginBottom:8 }}>{fmt(Wtotal)}</div>
            {WEntry.map(e => {
              const contrib = (counts[e.id]||0)*e.A*e.Zf;
              const frac = Wtotal > 0 ? contrib/Wtotal : 0;
              return (
                <div key={e.id} style={{ marginBottom:5 }}>
                  <div style={{ display:"flex", justifyContent:"space-between", fontSize:10 }}>
                    <span style={{ color:e.col }}>{e.id}</span>
                    <span style={{ fontFamily:MONO, color:GRY }}>{fmt(contrib)} ({(frac*100).toFixed(1)}%)</span>
                  </div>
                  <div style={{ height:3, background:DIM, borderRadius:1, marginTop:2 }}>
                    <div style={{ width:`${frac*100}%`, height:"100%", background:e.col, borderRadius:1 }}/>
                  </div>
                </div>
              );
            })}
          </div>
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:4, padding:"14px 16px" }}>
            <div style={{ fontSize:11, color:GRY, marginBottom:8 }}>New aeon particle budget N′</div>
            <input type="number" value={Nprime} onChange={e => setNprime(parseFloat(e.target.value)||1e9)}
              style={{ width:"100%", background:"#0a0a18", border:`1px solid ${BRD}`, color:TXT, fontFamily:MONO, fontSize:11, padding:"5px 10px", borderRadius:3, marginBottom:10 }}/>
            <div style={{ display:"flex", justifyContent:"space-between", fontSize:11, marginBottom:6 }}>
              <span style={{ color:GRY }}>Max W (all Up):</span>
              <span style={{ fontFamily:MONO, color:GRN }}>{fmt(WmaxLight)}</span>
            </div>
            <div style={{ display:"flex", justifyContent:"space-between", fontSize:11, marginBottom:10 }}>
              <span style={{ color:GRY }}>Required Wtotal:</span>
              <span style={{ fontFamily:MONO, color:PRP }}>{fmt(Wtotal)}</span>
            </div>
            <div style={{ background:needsHeavy?"#1a0a1a":"#0a1a0a", border:`1px solid ${needsHeavy?PRP+"44":GRN+"44"}`, borderLeft:`2px solid ${needsHeavy?PRP:GRN}`, borderRadius:3, padding:"10px 12px" }}>
              <div style={{ fontFamily:MONO, fontSize:9, color:needsHeavy?PRP:GRN, letterSpacing:1, marginBottom:4 }}>
                {needsHeavy ? "▲ HEAVY-FERMION DOMINATED AEON" : "▼ LIGHT-FERMION DOMINATED AEON"}
              </div>
              <div style={{ fontSize:11, color:GRY, lineHeight:1.6 }}>
                {needsHeavy
                  ? `W deficit ×${fmt(Wtotal/WmaxLight)} above light-quark ceiling. Vacuum forced into high-W inverted states.`
                  : "Wtotal satisfiable with light quarks. New aeon seeds a low-energy mass hierarchy."}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 5-7 — GENERATION CARDS (shared renderer)
// ══════════════════════════════════════════════════════════════
function GenCard({ p, insight }) {
  const pred = mass(p.A, p.Zf, p.L); const ec = errColor(pct(pred, p.obs));
  return (
    <div style={{ background:PNL, border:`1px solid ${p.col}`, borderTop:`3px solid ${p.col}`, borderRadius:6, padding:"20px" }}>
      <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:10 }}>
        <div style={{ fontFamily:MONO, fontSize:18, color:p.col }}>{p.label}</div>
        <Tag label={p.tag} col={p.col}/>
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginBottom:12 }}>
        {p.stats.map(([k,v]) => (
          <div key={k} style={{ background:DIM, borderRadius:3, padding:"8px 10px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, marginBottom:2 }}>{k}</div>
            <div style={{ fontFamily:MONO, fontSize:12, color:AMB }}>{v}</div>
          </div>
        ))}
      </div>
      <div style={{ fontSize:11, color:GRY, lineHeight:1.75, marginBottom:14 }}>{p.desc}</div>
      <div style={{ borderTop:`1px solid ${BRD}`, paddingTop:10, display:"flex", justifyContent:"space-between", fontSize:11 }}>
        <span style={{ color:GRY }}>Predicted</span>
        <span style={{ fontFamily:MONO, color:ec }}>{fmtMeV(pred)} ({pct(pred,p.obs)>=0?"+":""}{pct(pred,p.obs).toFixed(2)}%)</span>
      </div>
    </div>
  );
}
function GenIKnotMap() {
  return (
    <div>
      <SectionHead col={GRN}>GENERATION I · THE FANO-RESONANCE BASE LAYER</SectionHead>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:24, marginBottom:20 }}>
        <GenCard p={{ label:"Up Quark", knot:"3₁", A:3, Zf:3, L:16.372, obs:2.16, col:GRN, tag:"MINIMAL RESONANCE",
          stats:[["Knot / A","3₁ · A=3"],["Zf","3"],["L","16.372 fm"]],
          desc:"The 3₁ trefoil is the simplest knotted manifold. It aligns with the foundational 3D structure of the vacuum (Zf = 3), finding immediate stability at a 1:1 phase ratio per dimension." }}/>
        <GenCard p={{ label:"Down Quark", knot:"4₁", A:11, Zf:9, L:21.04, obs:4.70, col:CYA, tag:"AMPHICHEIRAL TORQUE",
          stats:[["Knot / A","4₁ · A=11"],["Zf","9 (3²)"],["L","21.04 fm"]],
          desc:"The 4₁ figure-eight knot is fully amphicheiral — no intrinsic handedness. This symmetry conflict in a chiral vacuum generates topological torque, squaring the base Fano resonance (3² = 9)." }}/>
      </div>
      <div style={{ background:"#0a1a0a", border:`1px solid ${GRN}44`, borderLeft:`3px solid ${GRN}`, borderRadius:4, padding:"14px 18px" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:GRN, letterSpacing:2, marginBottom:6 }}>GROUND STATE FOUNDATION</div>
        <div style={{ fontSize:11, color:GRY, lineHeight:1.75 }}>Zf = 3 for the Up quark is the geometric anchor for the entire framework. Every subsequent generation's mass is a scaling, inversion, or breaking of this Fano base.</div>
      </div>
    </div>
  );
}
function GenIIKnotMap() {
  return (
    <div>
      <SectionHead col={ORG}>GENERATION II · THE PLATONIC SYMMETRY PAIRING</SectionHead>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:24, marginBottom:20 }}>
        <GenCard p={{ label:"Strange Quark", A:107, Zf:12, L:29.13, obs:93.5, col:"#f59e0b", tag:"TETRAHEDRAL SUPPRESSION",
          stats:[["Knot / A","6₁ · A=107"],["Zf","12 (T⊂O)"],["1/Zf","0.083×"]],
          desc:"The 6₁ knot is topologically massive (A=107). The chiral tetrahedral group T (order 12) distributes energy across 12 rotational symmetries, heavily suppressing the base mass." }}/>
        <GenCard p={{ label:"Charm Quark", A:5, Zf:1/48, L:23.60, obs:1273.0, col:ORG, tag:"OCTAHEDRAL INVERSION",
          stats:[["Knot / A","5₁ · A=5"],["Zf","1/48"],["1/Zf","48× amplifier"]],
          desc:"The 5₁ knot is topologically tiny (A=5). The full bilateral octahedral group O_h (order 48) inverts the phase, making Zf fractional — a 48× energy multiplier." }}/>
      </div>
      <div style={{ background:"#1a0a00", border:`1px solid ${ORG}44`, borderLeft:`3px solid ${ORG}`, borderRadius:4, padding:"14px 18px" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:ORG, letterSpacing:2, marginBottom:6 }}>THE MASS INVERSION PARADOX</div>
        <div style={{ fontSize:11, color:GRY, lineHeight:1.75 }}>The Strange knot (A=107) is topologically far larger than Charm (A=5), yet Charm is 13× heavier. Mass is governed by the Platonic symmetries acting on the knot — not the knot's native size.</div>
      </div>
    </div>
  );
}
function GenIIIKnotMap() {
  const mBase = mass(119, 1,           37.31);
  const botPred = mass(119, 0.75,       37.31);
  const topPred = mass(119, 1/(8*phi4), 37.31);
  return (
    <div>
      <SectionHead col={PRP}>GENERATION III · THE 8₁ MANIFOLD SYMMETRY BREAKING</SectionHead>
      <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"14px 20px", textAlign:"center", marginBottom:14 }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:3, marginBottom:6 }}>UNATTENUATED BASE KNOT (Zf = 1)</div>
        <div style={{ fontFamily:MONO, fontSize:18, color:TXT, marginBottom:4 }}>8₁ · A = 119 · L = 37.31 fm</div>
        <div style={{ fontFamily:MONO, fontSize:14, color:AMB }}>m_base = {fmtMeV(mBase)}</div>
        <div style={{ fontSize:11, color:GRY, marginTop:6 }}>Both Bottom and Top share this knot. All mass difference is vacuum phase only.</div>
      </div>
      <div style={{ textAlign:"center", fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:14, padding:"6px 0", borderTop:`1px solid ${BRD}`, borderBottom:`1px solid ${BRD}` }}>↕  VACUUM PHASE LOCK BIFURCATION</div>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:24, marginBottom:20 }}>
        {[
          { label:"Bottom Quark", Zf:0.75, col:"#60a5fa", tag:"RELAXED STATE", pred:botPred, obs:4183,
            stats:[["Zf","3/4"],["1/Zf","1.333×"]],
            desc:"C₃/C₄ phase lock. The 8₁ manifold achieves stable fractional alignment, locking 3 of 4 structural quadrants and experiencing mild topological drag." },
          { label:"Top Quark (8₁⁹)", Zf:1/(8*phi4), col:RED, tag:"HYPER-COMPRESSED", pred:topPred, obs:172570,
            stats:[["Zf","1/(8φ⁴)"],["1/Zf",`${(8*phi4).toFixed(3)}×`]],
            desc:"Full bulk modulus over the cubic vacuum (κ/8 = 1/(8φ⁴)). The manifold is fully crushed by the 8-dimensional vacuum modulus, creating maximum topological drag." },
        ].map(p => {
          const ec = errColor(pct(p.pred,p.obs));
          return (
            <div key={p.label} style={{ background:PNL, border:`1px solid ${p.col}`, borderTop:`3px solid ${p.col}`, borderRadius:6, padding:"20px" }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:10 }}>
                <div style={{ fontFamily:MONO, fontSize:17, color:p.col }}>{p.label}</div>
                <Tag label={p.tag} col={p.col}/>
              </div>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginBottom:12 }}>
                {p.stats.map(([k,v]) => (
                  <div key={k} style={{ background:DIM, borderRadius:3, padding:"8px 10px" }}>
                    <div style={{ fontFamily:MONO, fontSize:9, color:GRY, marginBottom:2 }}>{k}</div>
                    <div style={{ fontFamily:MONO, fontSize:13, color:AMB }}>{v}</div>
                  </div>
                ))}
              </div>
              <div style={{ fontSize:11, color:GRY, lineHeight:1.75, marginBottom:14 }}>{p.desc}</div>
              <div style={{ borderTop:`1px solid ${BRD}`, paddingTop:10, display:"flex", justifyContent:"space-between", fontSize:11 }}>
                <span style={{ color:GRY }}>Predicted</span>
                <span style={{ fontFamily:MONO, color:ec }}>{fmtMeV(p.pred)} ({pct(p.pred,p.obs)>=0?"+":""}{pct(p.pred,p.obs).toFixed(2)}%)</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 8 — LEPTONS
// ══════════════════════════════════════════════════════════════
function LeptonKnotMap() {
  const L0 = L_q;  // L_q = PHI*phi² ≈ 16.363 (canonical lepton companion ropelength)
  const ePred   = mass(1, 1,          TWO_PI);
  const muPred  = mass(1, ZF_LEPTON, 2*L0);
  const tauPred = mass(3, ZF_LEPTON, 3*L0);
  return (
    <div>
      <SectionHead col="#818cf8">LEPTON CABLING SEQUENCE · LOOP-PERIOD STABILIZER Zf = 1/2π (v1.8)</SectionHead>
      <div style={{ background:PNL, border:`1px solid #818cf8`, borderTop:`2px solid #818cf8`, borderRadius:6, padding:"16px 20px", marginBottom:14 }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:10 }}>WHY Zf = 1/(2π) FOR HEAVY LEPTONS</div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:16, fontSize:11, color:GRY, lineHeight:1.8 }}>
          <div><div style={{ fontFamily:MONO, fontSize:10, color:"#818cf8", marginBottom:4 }}>2π already in SQT</div>2π is the electron's ropelength (L=2π) and the dominant term in Φ = 2π + K(0)/8π². Not a new constant.</div>
          <div><div style={{ fontFamily:MONO, fontSize:10, color:"#818cf8", marginBottom:4 }}>Inversion → amplifier</div>Zf = 1/(2π) gives 1/Zf = 2π ≈ 6.283. Same inversion mechanism as Top (1/8φ⁴) and Charm (1/48) — no new logic.</div>
          <div><div style={{ fontFamily:MONO, fontSize:10, color:"#818cf8", marginBottom:4 }}>Split by topology alone</div>Muon and Tau share Zf = 1/(2π). Mass ratio determined entirely by A: Muon unknot (A=1), Tau trefoil (A=3).</div>
        </div>
      </div>
      <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"12px 20px", textAlign:"center", marginBottom:14 }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:3, marginBottom:4 }}>TRIVIAL GROUND STATE</div>
        <div style={{ fontFamily:MONO, fontSize:18, color:"#60a5fa", marginBottom:4 }}>Electron (0₁) — A=1, Zf=1, L=2π</div>
        <div style={{ fontFamily:MONO, fontSize:12, color:errColor(pct(ePred,0.511)) }}>{fmtMeV(ePred)} ({pct(ePred,0.511)>=0?"+":""}{pct(ePred,0.511).toFixed(3)}%)</div>
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20, marginBottom:14 }}>
        {[
          { label:"Muon", A:1, L:2*L0, obs:105.658, pred:muPred, col:"#a78bfa", tag:"GEN II — UNKNOT CABLE",
            desc:"Cables the unknot (0₁) twice. A=1, stabilizer locks to 1/(2π), so mass amplifier is simply 2π — the most minimal non-trivial multiplier in the framework.", amplifier:`A/Zf = 1 × 2π = ${(2*Math.PI).toFixed(4)}` },
          { label:"Tau", A:3, L:3*L0, obs:1776.93, pred:tauPred, col:"#c084fc", tag:"GEN III — TREFOIL CABLE",
            desc:"Cables the trefoil (3₁) three times. Trefoil core contributes A=3. Sharing Zf = 1/(2π) with Muon means the τ/μ mass ratio is a pure topological ratio.", amplifier:`A/Zf = 3 × 2π = ${(6*Math.PI).toFixed(4)}` },
        ].map(p => {
          const err = pct(p.pred, p.obs); const ec = errColor(err);
          return (
            <div key={p.label} style={{ background:PNL, border:`1px solid ${p.col}`, borderTop:`3px solid ${p.col}`, borderRadius:6, padding:"20px" }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:10 }}>
                <div style={{ fontFamily:MONO, fontSize:20, color:p.col }}>{p.label}</div>
                <Tag label={p.tag} col={p.col}/>
              </div>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginBottom:12 }}>
                {[["A / Zf",`${p.A} / 2π`],["L",`${p.L.toFixed(3)} fm`],["Amplifier",p.amplifier]].map(([k,v]) => (
                  <div key={k} style={{ background:DIM, borderRadius:3, padding:"8px 10px" }}>
                    <div style={{ fontFamily:MONO, fontSize:9, color:GRY, marginBottom:2 }}>{k}</div>
                    <div style={{ fontFamily:MONO, fontSize:11, color:AMB }}>{v}</div>
                  </div>
                ))}
              </div>
              <div style={{ fontSize:11, color:GRY, lineHeight:1.75, marginBottom:14 }}>{p.desc}</div>
              <div style={{ borderTop:`1px solid ${BRD}`, paddingTop:10, display:"flex", justifyContent:"space-between", fontSize:11 }}>
                <span style={{ color:GRY }}>Predicted</span>
                <span style={{ fontFamily:MONO, color:ec, fontWeight:700 }}>{fmtMeV(p.pred)} ({err>=0?"+":""}{err.toFixed(3)}%)</span>
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ background:"#0a0a14", border:`1px solid #818cf844`, borderLeft:`3px solid #818cf8`, borderRadius:4, padding:"14px 18px" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:"#818cf8", letterSpacing:2, marginBottom:6 }}>v1.7 → v1.8 CORRECTION</div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20, fontSize:11, color:GRY, lineHeight:1.75 }}>
          <div><strong style={{ color:RED }}>v1.7 (wrong):</strong> Muon A=3, Zf=3 → 15.6 MeV (−85%). Tau A=3, Zf=3 → 93 MeV (−95%). The reff logarithmic correction destroyed both predictions.</div>
          <div><strong style={{ color:GRN }}>v1.8 (corrected):</strong> Muon A=1, Zf=1/2π → {fmtMeV(muPred)} ({pct(muPred,105.658).toFixed(2)}%). Tau A=3, Zf=1/2π → {fmtMeV(tauPred)} ({pct(tauPred,1776.93).toFixed(2)}%). Tau is now precision-class.</div>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 9 — FORCE-RESIDUAL
// ══════════════════════════════════════════════════════════════
function ForceResidual() {
  const [selected, setSelected] = useState(null);
  const forces = [
    { r:0, label:"r = 0", force:"Strong (SU(3))", bosons:"8 gluons", mass:"confined", drag:"D(0)=0", col:RED,
      desc:"All 8 color edges fully satisfied by SU(3) crystallization. Zero free propagating degrees of freedom → color confinement. 6 directional generators + 2 Cartan diagonal generators = 8 gluons via Fano-to-SU(3) bridge." },
    { r:1, label:"r = 1", force:"Electromagnetism (U(1))", bosons:"γ photon", mass:"massless", drag:"D(1)=1/3→0", col:AMB,
      desc:"One free edge → one degree of freedom: phase angle θ in [0, 2π) — topology of S¹. Zero topological drag implies zero acquired mass. The photon is massless because its residual channel is geometrically frictionless." },
    { r:2, label:"r = 2", force:"FORBIDDEN", bosons:"—", mass:"unstable", drag:"D(2)=2/3 (saddle)", col:GRY, forbidden:true,
      desc:"A 2D planar channel creates asymmetric topological torque — the plane of propagation is stabilised but the orthogonal axis carries unbalanced residual stress. D(2)=2/3 is a free-energy saddle point. Any perturbation drives the system to r=1 or r=3." },
    { r:3, label:"r = 3", force:"Weak (SU(2))", bosons:"W⁺ W⁻ Z⁰", mass:"~80 GeV", drag:"D(3)=3/3=1", col:CYA,
      desc:"Three edges share a vacuum node → common phase constraint. Minimal Lie group with 3 coupled generators closing under the Lie bracket = SU(2). Full volumetric resistance D=1 → maximum drag → mass acquisition." },
  ];
  const sel = forces.find(f => f.r === selected);
  return (
    <div>
      <SectionHead col={RED}>THEOREM 3 · FORCE-RESIDUAL CORRESPONDENCE FROM MOD-8 DIMENSIONALITY</SectionHead>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
        <div>
          {forces.map(f => (
            <div key={f.r} onClick={() => setSelected(selected===f.r?null:f.r)}
              style={{ background:selected===f.r?PNL:DIM, border:`1px solid ${selected===f.r?f.col:BRD}`, borderLeft:`3px solid ${f.col}`, borderRadius:4, padding:"12px 16px", marginBottom:8, cursor:"pointer", opacity:f.forbidden?0.7:1 }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:6 }}>
                <div style={{ display:"flex", gap:10, alignItems:"center" }}>
                  <span style={{ fontFamily:MONO, fontSize:18, color:f.col, fontWeight:700 }}>{f.label}</span>
                  {f.forbidden && <Tag label="FORBIDDEN" col={GRY}/>}
                </div>
                <span style={{ fontFamily:MONO, fontSize:10, color:GRY }}>{f.drag}</span>
              </div>
              <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:6 }}>
                {[["Force",f.force],["Bosons",f.bosons],["Mass",f.mass]].map(([k,v]) => (
                  <div key={k}><div style={{ fontSize:8, color:GRY, fontFamily:MONO, marginBottom:2 }}>{k}</div><div style={{ fontSize:10, color:f.col }}>{v}</div></div>
                ))}
              </div>
            </div>
          ))}
          <div style={{ background:"#0a0a1a", border:`1px solid ${GRY}33`, borderRadius:4, padding:"12px 14px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:6 }}>r=2 TRANSIENT BSM PREDICTION</div>
            <div style={{ fontSize:11, color:GRY, lineHeight:1.7 }}>
              If r=2 accessible at extreme energies:<br/>
              • 2 gauge bosons · mass ≈ (2/3)·mW ≈ <span style={{ color:AMB }}>53 GeV</span><br/>
              • Coupling to 2D planar degrees of freedom
            </div>
          </div>
        </div>
        <div>
          {sel ? (
            <div style={{ background:PNL, border:`1px solid ${sel.col}`, borderTop:`2px solid ${sel.col}`, borderRadius:4, padding:"18px 20px" }}>
              <div style={{ fontFamily:MONO, fontSize:22, color:sel.col, marginBottom:4 }}>{sel.label}</div>
              <div style={{ fontSize:15, color:TXT, marginBottom:12 }}>{sel.force}</div>
              <div style={{ fontSize:11, color:GRY, lineHeight:1.8, marginBottom:16 }}>{sel.desc}</div>
              <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:6 }}>TOPOLOGICAL DRAG D(r) = r/3</div>
              <div style={{ height:16, background:DIM, borderRadius:8, overflow:"hidden", marginBottom:4 }}>
                <div style={{ width:`${[0,33.3,66.6,100][sel.r]}%`, height:"100%", background:sel.forbidden?GRY:`linear-gradient(90deg,${GRN},${sel.col})`, transition:"width 0.4s", borderRadius:8 }}/>
              </div>
              <div style={{ display:"flex", justifyContent:"space-between", fontSize:9, color:GRY }}>
                <span>0 (frictionless)</span>
                <span>D={sel.r}/3={(sel.r/3).toFixed(3)}</span>
                <span>1 (full drag)</span>
              </div>
            </div>
          ) : (
            <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:4, padding:"20px", display:"flex", alignItems:"center", justifyContent:"center", minHeight:280, color:GRY, fontFamily:MONO, fontSize:11 }}>
              ← Select a residual to view derivation
            </div>
          )}
          <div style={{ marginTop:12, background:DIM, border:`1px solid ${BRD}`, borderRadius:4, padding:"12px 16px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>FORCE MAP</div>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:6 }}>
              {[{r:"0",c:RED,g:"SU(3)"},{r:"1",c:AMB,g:"U(1)"},{r:"2",c:GRY,g:"—"},{r:"3",c:CYA,g:"SU(2)"}].map(x => (
                <div key={x.r} style={{ background:PNL, border:`1px solid ${x.c}33`, borderTop:`2px solid ${x.c}`, borderRadius:3, padding:"8px 10px", textAlign:"center" }}>
                  <div style={{ fontFamily:MONO, fontSize:15, color:x.c }}>r={x.r}</div>
                  <div style={{ fontFamily:MONO, fontSize:9, color:GRY, marginTop:2 }}>{x.g}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 10 — NEUTRINOS
// ══════════════════════════════════════════════════════════════
function NeutrinoSector() {
  // Zf_nu = ξvac³: dimensional (3D correlation volume) argument, NOT derived
  // from PSL(2,7) stabilizer modes. Conjecture only — see Paper VII Open Problem.
  const Zf_nu  = Math.pow(XI_VAC, 3);
  const m_nu   = m0 / Zf_nu;  // mass(A=1, Zf=Zf_nu, L=0): unclosed defect limit
  const m_nu_eV = m_nu * 1e6;
  return (
    <div>
      <SectionHead col="#38bdf8">THE NEUTRINO SECTOR · VOLUMETRIC PHASE DELOCALIZATION</SectionHead>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20, marginBottom:20 }}>
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"20px" }}>
          <div style={{ fontFamily:MONO, fontSize:20, color:"#38bdf8", marginBottom:10 }}>The Topological Ghost</div>
          <div style={{ fontSize:11, color:GRY, lineHeight:1.8, marginBottom:14 }}>
            The Electron is a closed unknot (L=2π) that anchors to the local vacuum phase (Zf=1). A Neutrino is a topological slip — an unclosed defect with L→0. It stabilizes against the entire 3D correlation volume.
          </div>
          <div style={{ background:DIM, borderLeft:`3px solid #38bdf8`, borderRadius:3, padding:"12px 14px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:"#38bdf8", letterSpacing:1, marginBottom:4 }}>VOLUMETRIC STABILIZER</div>
            <div style={{ fontFamily:MONO, fontSize:13, color:TXT }}>Zf = ξvac³ = (100φ)³</div>
            <div style={{ fontFamily:MONO, fontSize:11, color:AMB, marginTop:4 }}>≈ {Math.round(Zf_nu).toLocaleString()}</div>
          </div>
        </div>
        <div>
          <div style={{ background:"#020b14", border:`1px solid #38bdf8`, borderTop:`3px solid #38bdf8`, borderRadius:4, padding:"18px", marginBottom:12 }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:6 }}>PREDICTED PRIMARY EIGENSTATE MASS</div>
            <div style={{ fontFamily:MONO, fontSize:36, color:"#38bdf8", marginBottom:4 }}>{m_nu_eV.toFixed(4)} eV</div>
            <div style={{ height:4, background:DIM, borderRadius:2, overflow:"hidden", marginBottom:4 }}>
              <div style={{ width:`${Math.min(100,(m_nu_eV/0.12)*100)}%`, height:"100%", background:"#38bdf8" }}/>
            </div>
            <div style={{ display:"flex", justifyContent:"space-between", fontSize:9, color:GRY }}>
              <span>0 eV</span><span style={{ color:GRN }}>0.12 eV Planck upper bound</span>
            </div>
          </div>
          <div style={{ background:DIM, borderRadius:4, padding:"12px 14px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>FLAVOR OSCILLATIONS</div>
            <div style={{ fontSize:11, color:GRY, lineHeight:1.75 }}>Without a geometric lock (L=0), neutrino flavor is a transient phase-interference pattern. No seesaw mechanism required.</div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 11 — WEAK BOSONS
// ══════════════════════════════════════════════════════════════
function ElectroweakSector() {
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

// ══════════════════════════════════════════════════════════════
//  TAB 12 — LENS EQUATION
// ══════════════════════════════════════════════════════════════
function LensEquation() {
  const [pid, setPid]   = useState("top");
  const [n, setN]       = useState(1);
  const [dphi, setDphi] = useState(0);
  const p       = PARTICLES.find(x => x.id === pid);
  const hf0     = mass(p.A, p.Zf, p.L);
  const atten   = Math.exp(-kappa * n);
  const phase   = Math.pow(Math.cos(dphi), 2);
  const Edet    = hf0 * atten * phase;
  const fidelity = Edet / hf0 * 100;
  const floor   = Math.exp(-kappa) * 100;
  return (
    <div>
      <SectionHead col={ORG}>SECTION 8 · SQT LENS EQUATION — S-MATRIX DISSIPATION</SectionHead>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
        <div>
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:4, padding:"16px 18px", marginBottom:14 }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:10 }}>INVARIANT VERTEX SOURCE (hf₀)</div>
            <div style={{ display:"flex", flexWrap:"wrap", gap:6, marginBottom:14 }}>
              {PARTICLES.map(px => (
                <button key={px.id} onClick={() => setPid(px.id)} style={{ background:pid===px.id?PNL:"transparent", border:`1px solid ${pid===px.id?px.col:BRD}`, color:pid===px.id?px.col:GRY, padding:"3px 10px", borderRadius:3, fontFamily:MONO, fontSize:9, cursor:"pointer" }}>{px.label}</button>
              ))}
            </div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, marginBottom:14 }}>
              <div style={{ background:DIM, borderRadius:3, padding:"8px 10px" }}>
                <div style={{ fontSize:9, color:GRY, fontFamily:MONO }}>VERTEX MASS hf₀</div>
                <div style={{ fontFamily:MONO, fontSize:13, color:CYA, marginTop:3 }}>{fmtMeV(hf0)}</div>
              </div>
              <div style={{ background:DIM, borderRadius:3, padding:"8px 10px" }}>
                <div style={{ fontSize:9, color:GRY, fontFamily:MONO }}>KNOT</div>
                <div style={{ fontFamily:MONO, fontSize:12, color:p.col, marginTop:3 }}>{p.knot}</div>
              </div>
            </div>
            <Slider label="n — Zf layer transitions" min={1} max={8} step={1} value={n} onChange={setN} col={ORG}/>
            <Slider label="Δφ — phase misalignment (rad)" min={0} max={Math.PI/2} step={0.01} value={dphi} onChange={setDphi} display={`${dphi.toFixed(3)} rad (${(dphi/(Math.PI/2)*90).toFixed(1)}°)`} col={PRP}/>
          </div>
          <div style={{ background:DIM, border:`1px solid ${BRD}`, borderRadius:4, padding:"14px 16px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>LENS EQUATION</div>
            <div style={{ fontFamily:MONO, fontSize:12, color:ORG, lineHeight:1.9 }}>
              E_det = hf₀ · e^(−αn) · cos²(Δφ)<br/>
              <span style={{ color:GRY }}>α = κ = 1/φ⁴ = {kappa.toFixed(6)}</span>
            </div>
          </div>
        </div>
        <div>
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderTop:`2px solid ${ORG}`, borderRadius:4, padding:"20px 22px", marginBottom:14 }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>SIGNAL FIDELITY</div>
            <div style={{ fontFamily:MONO, fontSize:36, color:fidelity>80?GRN:fidelity>50?AMB:RED, marginBottom:4 }}>{fidelity.toFixed(2)}%</div>
            <div style={{ fontFamily:MONO, fontSize:14, color:TXT, marginBottom:14 }}>{fmtMeV(Edet)} detected</div>
            <div style={{ position:"relative", height:18, background:DIM, borderRadius:9, overflow:"hidden", marginBottom:6 }}>
              <div style={{ width:`${Math.max(0,fidelity)}%`, height:"100%", background:`linear-gradient(90deg,${RED},${AMB},${GRN})`, transition:"width 0.3s", borderRadius:9 }}/>
              <div style={{ position:"absolute", top:0, left:`${floor}%`, width:2, height:"100%", background:AMB }}/>
            </div>
            <div style={{ display:"flex", justifyContent:"space-between", fontSize:9, color:GRY }}>
              <span>0% (total dissipation)</span>
              <span style={{ color:AMB }}>↑ n=1 floor ({floor.toFixed(1)}%)</span>
              <span>100% (hf₀)</span>
            </div>
          </div>
          <div style={{ background:"#0f0a00", border:`1px solid ${AMB}44`, borderLeft:`2px solid ${AMB}`, borderRadius:4, padding:"12px 14px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:AMB, letterSpacing:1, marginBottom:4 }}>OBSERVATIONAL CEILING</div>
            <div style={{ fontSize:11, color:GRY, lineHeight:1.7 }}>
              No measurement can exceed e^(−κ)·hf₀ ≈ {floor.toFixed(2)}% of vertex energy. This {(100-floor).toFixed(1)}% floor is the irreducible thermodynamic cost of a single Zf layer traversal — geometric, not instrumental.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 13 — COSMIC ECHOES
// ══════════════════════════════════════════════════════════════
function CosmologicalEchoes() {
  const [src, setSrc] = useState(100);
  const Fg    = kappa / 4;
  const trans = Math.exp(-Fg);
  const surv  = src * trans;
  return (
    <div>
      <SectionHead col={CYA}>COSMOLOGICAL BOUNDARY TRANSMITTANCE</SectionHead>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20, marginBottom:16 }}>
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"20px" }}>
          <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:10 }}>GRAVITY AS VACUUM GEOMETRY</div>
          <div style={{ fontSize:11, color:GRY, lineHeight:1.8, marginBottom:14 }}>Gravity is not an r-residual force — it is the fundamental geometry of the superfluid medium itself (K(0) = −φ²). Gravitational waves can cross the conformal boundary, resisted by the bulk modulus across all 4 spacetime dimensions.</div>
          <div style={{ background:DIM, borderLeft:`3px solid ${CYA}`, borderRadius:3, padding:"12px 14px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:CYA, letterSpacing:1, marginBottom:4 }}>4D FILTRATION CONSTANT</div>
            <div style={{ fontFamily:MONO, fontSize:13, color:TXT }}>F_g = κ/4 = 1/(4φ⁴) = {Fg.toFixed(8)}</div>
          </div>
        </div>
        <div>
          <Slider label="Initial echo amplitude (%)" min={1} max={100} step={1} value={src} onChange={setSrc} display={`${src}%`} col={CYA}/>
          <div style={{ background:PNL, border:`1px solid ${CYA}`, borderTop:`3px solid ${CYA}`, borderRadius:4, padding:"18px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:6 }}>AEON N+1 SURVIVING ENERGY</div>
            <div style={{ fontFamily:MONO, fontSize:36, color:CYA, marginBottom:4 }}>{surv.toFixed(3)}%</div>
            <div style={{ fontFamily:MONO, fontSize:12, color:RED, marginBottom:12 }}>Dissipated: −{(src-surv).toFixed(3)}%</div>
            <div style={{ height:6, background:DIM, borderRadius:3, overflow:"hidden", display:"flex", marginBottom:4 }}>
              <div style={{ width:`${surv}%`, height:"100%", background:CYA }}/>
              <div style={{ width:`${src-surv}%`, height:"100%", background:RED }}/>
            </div>
            <div style={{ fontSize:9, color:GRY, marginTop:4 }}>Transmittance: exp(−κ/4) ≈ {(trans*100).toFixed(4)}%</div>
          </div>
        </div>
      </div>
      <div style={{ background:"#0a0a14", border:`1px solid ${CYA}44`, borderLeft:`3px solid ${CYA}`, borderRadius:4, padding:"14px 18px" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:CYA, letterSpacing:2, marginBottom:6 }}>PRIOR AEON FOSSIL RECORD</div>
        <div style={{ fontSize:11, color:GRY, lineHeight:1.75 }}>~{(trans*100).toFixed(2)}% of a gravitational echo's Worticity signature survives the conformal crossover. This explains why supermassive black hole collision signatures may leave concentric ring patterns in the CMB temperature anisotropy.</div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 14 — FREEZE-OUT
// ══════════════════════════════════════════════════════════════
function ThermodynamicFreezeOut() {
  const EVENTS = [
    { label:"Top (8₁⁹)",   Tc:172000,  col:RED       },
    { label:"W/Z Bosons",  Tc:80400,   col:PRP       },
    { label:"Bottom (8₁)", Tc:4180,    col:"#60a5fa" },
    { label:"Tau Lepton",  Tc:1776,    col:"#c084fc" },
    { label:"Charm",       Tc:1270,    col:ORG       },
    { label:"Strange",     Tc:93,      col:AMB       },
    { label:"Muon Lepton", Tc:106,     col:"#a78bfa" },
    { label:"Up / Down",   Tc:3.4,     col:GRN       },
    { label:"Electron",    Tc:0.511,   col:"#818cf8" },
    { label:"Neutrino",    Tc:4.41e-8, col:"#38bdf8" },
  ].sort((a,b) => b.Tc - a.Tc);
  const maxLog = 5.3; const minLog = -10; const span = maxLog - minLog;
  const W = 900; const H = 300;
  const getX = logT => ((maxLog - logT) / span * 88 + 6);
  function sCurve(Tc) {
    let d = "";
    for (let i=0; i<=200; i++) {
      const logT = maxLog - (i/200)*span;
      const z = 1 / (1 + Math.exp(10*(logT - Math.log10(Tc))));
      const x = getX(logT)/100 * W;
      const y = H - 20 - z*(H-50);
      d += `${i===0?"M":"L"} ${x.toFixed(1)} ${y.toFixed(1)} `;
    }
    return d;
  }
  return (
    <div>
      <SectionHead col={AMB}>THEOREM 2 EXTENSION · THERMODYNAMIC FREEZE-OUT CURVE</SectionHead>
      <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"20px", marginBottom:14 }}>
        <div style={{ overflowX:"auto" }}>
          <svg viewBox={`0 0 ${W} ${H+50}`} width="100%" style={{ fontFamily:MONO }}>
            {[5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10].map(t => {
              const x = getX(t)/100*W;
              const labels = {5:"100 GeV",3:"1 GeV",0:"1 MeV","-3":"1 keV","-6":"1 eV","-9":"1 meV"};
              return (
                <g key={t}>
                  <line x1={x} y1={18} x2={x} y2={H-18} stroke={DIM} strokeWidth="1" strokeDasharray="3 3"/>
                  {labels[String(t)] && <text x={x} y={H+12} fill={GRY} fontSize="8" textAnchor="middle">{labels[String(t)]}</text>}
                </g>
              );
            })}
            <text x="4" y="28" fill={GRY} fontSize="8">ζ=1</text>
            <text x="4" y={H-14} fill={GRY} fontSize="8">ζ=0</text>
            <text x={W/2} y={H+38} fill={AMB} fontSize="8" textAnchor="middle">← EARLY UNIVERSE (HOT)          LATE UNIVERSE (COLD) →</text>
            {EVENTS.map((e, i) => {
              const logTc = Math.log10(e.Tc);
              const cx    = getX(logTc)/100*W;
              const labelY = 32 + (i % 5) * 18;
              return (
                <g key={e.label}>
                  <path d={sCurve(e.Tc)} fill="none" stroke={e.col} strokeWidth="1.6" opacity="0.8" strokeLinecap="round"/>
                  <circle cx={cx} cy={H/2} r="3" fill={BG} stroke={e.col} strokeWidth="1.6"/>
                  <text x={cx+4} y={labelY} fill={e.col} fontSize="7.5">{e.label}</text>
                </g>
              );
            })}
          </svg>
        </div>
      </div>
      <div style={{ overflowX:"auto" }}>
        <table style={{ width:"100%", borderCollapse:"collapse", fontFamily:MONO, fontSize:11 }}>
          <thead>
            <tr style={{ borderBottom:`1px solid ${BRD}` }}>
              {["#","Freeze-Out Tc","Particle"].map(h => (
                <th key={h} style={{ padding:"7px 10px", textAlign:"left", fontSize:9, color:GRY }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {EVENTS.map((e, i) => (
              <tr key={e.label} style={{ borderBottom:`1px solid ${DIM}`, background:i%2===0?"transparent":"#0d0d1a40" }}>
                <td style={{ padding:"7px 10px", color:GRY }}>{i+1}</td>
                <td style={{ padding:"7px 10px", color:TXT }}>{fmtMeV(e.Tc)}</td>
                <td style={{ padding:"7px 10px", color:e.col, fontWeight:700 }}>{e.label}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 15 — TOP QUARK Zf RESOLUTION  (merged from sqt_top_zf_comparison.jsx)
// ══════════════════════════════════════════════════════════════
const TOP_A = 119; const TOP_L = 37.31; const TOP_OBS = 172570;   // PDG 2024 direct measurement
const mBase = mass(TOP_A, 1, TOP_L);

const ZF_CANDIDATES = [
  { id:"legacy", label:"1/144",   Zf:1/144,         col:"#6b7280", verdict:"REJECTED",  verdictCol:RED,
    short:"Triple bilateral inversion",
    long:"Derived as (1/48) × (1/3) — Charm's octahedral inversion stacked twice then divided by the Fano base factor. Yields ~450 GeV, overshooting by 2.6×. The second inversion has no independent PSL(2,7) justification." },
  { id:"euler",  label:"e⁻⁴",    Zf:Math.exp(-4),  col:CYA,       verdict:"CANDIDATE", verdictCol:CYA,
    short:"Exponential 4D spacetime suppression",
    long:"Each spacetime dimension contributes one factor of e⁻¹ to the phase attenuation. The combined 4D suppression is e⁻⁴. Both e and D=4 already appear in the framework — no new constants introduced." },
  { id:"phi8",   label:"1/(8φ⁴)", Zf:1/(8*phi4),   col:PRP,       verdict:"SELECTED (FIT)", verdictCol:AMB,
    short:"Mod-8 vacuum × bulk modulus κ",
    long:"Zf = κ/8 = (1/φ⁴)/8 = 1/(8φ⁴). Combines κ = 1/φ⁴ (superfluid bulk modulus, Theorem 1) with b = 8 (the mod-8 base of Theorem 3; 8 = 2³, not 3³). Status (October 2026): a selected value — ledger §2.92 counts it among the six fitted Z_f." },
];

function TopZfTab() {
  const [selId, setSelId]   = useState("phi8");
  const [subtab, setSubtab] = useState("compare");
  const [mode, setMode]     = useState("phi");
  const [phiPow, setPhiPow] = useState(4);
  const [phiMul, setPhiMul] = useState(8);
  const [ePow, setEPow]     = useState(4);
  const [manVal, setManVal] = useState(1/144);

  const sel = ZF_CANDIDATES.find(x => x.id === selId);

  // Explorer live calc
  let exZf, exLabel;
  if (mode === "phi") { exZf = 1/(phiMul * Math.pow(phi,phiPow)); exLabel = `1/(${phiMul}φ^${phiPow})`; }
  else if (mode === "e") { exZf = Math.exp(-ePow); exLabel = `e^(−${ePow.toFixed(1)})`; }
  else { exZf = manVal; exLabel = "custom"; }
  const exPred = mBase / exZf;
  const exErr  = pct(exPred, TOP_OBS);
  const exEc   = errColor(exErr);

  const re = rEff(TOP_L);

  return (
    <div>
      <SectionHead col={PRP}>TOP QUARK Zf RESOLUTION · REPLACING 1/144</SectionHead>
      <div style={{ fontSize:11, color:GRY, lineHeight:1.7, marginBottom:14 }}>
        <span style={{ fontFamily:MONO, fontSize:9, color:AMB, letterSpacing:1 }}>STATUS · OCTOBER 2026 · </span>
        The candidates below are compared with the observed mass; whichever is kept is a fitted Z_f (ledger §2.92).
        Observed: PDG 2024, 172.57 ± 0.29 GeV.
      </div>

      {/* Three-way header */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:10, marginBottom:16 }}>
        {ZF_CANDIDATES.map(c => {
          const pred = mBase / c.Zf; const err = pct(pred, TOP_OBS); const ec = errColor(err);
          return (
            <div key={c.id} onClick={() => setSelId(c.id)}
              style={{ background:selId===c.id?PNL:DIM, border:`1px solid ${selId===c.id?c.col:BRD}`, borderTop:`3px solid ${c.col}`, borderRadius:4, padding:"12px 14px", cursor:"pointer", opacity:c.id==="legacy"?0.75:1 }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:6 }}>
                <span style={{ fontFamily:MONO, fontSize:18, color:c.col }}>{c.label}</span>
                <Tag label={c.verdict} col={c.verdictCol}/>
              </div>
              <div style={{ fontFamily:MONO, fontSize:13, color:TXT }}>{fmtMeV(pred)}</div>
              <div style={{ fontFamily:MONO, fontSize:12, color:ec, marginTop:2 }}>{err>=0?"+":""}{err.toFixed(3)}%</div>
              <div style={{ fontSize:9, color:GRY, marginTop:4 }}>{c.short}</div>
            </div>
          );
        })}
      </div>

      {/* Subtab bar */}
      <div style={{ display:"flex", gap:4, marginBottom:16 }}>
        {[["compare","Comparison",PRP],["table","Full Table",GRN],["explorer","Explorer",AMB]].map(([id,lbl,c]) => (
          <button key={id} onClick={() => setSubtab(id)} style={{ background:subtab===id?PNL:"transparent", border:`1px solid ${subtab===id?c:BRD}`, color:subtab===id?c:GRY, padding:"5px 14px", borderRadius:3, fontFamily:MONO, fontSize:9, cursor:"pointer" }}>{lbl.toUpperCase()}</button>
        ))}
      </div>

      {/* COMPARISON */}
      {subtab === "compare" && (
        <div>
          {/* Base derivation */}
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"18px 22px", marginBottom:16 }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:3, marginBottom:12 }}>STEP 0 — BASE KNOT ENERGY (Zf STRIPPED)</div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
              <div style={{ fontFamily:MONO, fontSize:11, color:GRY, lineHeight:2.1 }}>
                <span style={{ color:AMB }}>m_base</span> = m₀ · A · exp(L / Φ·reff)<br/>
                reff = 1 + ln(1 + {TOP_L}/{XI_VAC.toFixed(2)}) = <span style={{ color:AMB }}>{re.toFixed(6)}</span><br/>
                m_base = {m0.toFixed(6)} × {TOP_A} × exp({TOP_L.toFixed(2)}/{(PHI*re).toFixed(4)})<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= <span style={{ color:GRN, fontSize:14 }}>{fmtMeV(mBase)}</span>
              </div>
              <div style={{ background:DIM, borderRadius:4, padding:"14px 16px" }}>
                <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>TARGET 1/Zf</div>
                <div style={{ fontFamily:MONO, fontSize:13, color:TXT }}>172,570 MeV / {fmtMeV(mBase)}</div>
                <div style={{ fontFamily:MONO, fontSize:20, color:GRN, marginTop:4 }}>{(TOP_OBS/mBase).toFixed(4)}</div>
                <div style={{ fontSize:10, color:GRY, marginTop:6 }}>→ Zf_Top ≈ {(mBase/TOP_OBS).toFixed(6)}</div>
              </div>
            </div>
          </div>

          {/* Detail for selected */}
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:16 }}>
            <div style={{ background:PNL, border:`1px solid ${sel.col}`, borderTop:`2px solid ${sel.col}`, borderRadius:6, padding:"18px 20px" }}>
              <div style={{ fontFamily:MONO, fontSize:9, color:sel.col, letterSpacing:3, marginBottom:10 }}>{sel.label} — GEOMETRIC JUSTIFICATION</div>
              <div style={{ fontSize:11, color:GRY, lineHeight:1.85, marginBottom:14, whiteSpace:"pre-line" }}>{sel.long}</div>
              <div style={{ borderTop:`1px solid ${BRD}`, paddingTop:10 }}>
                <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:6 }}>CONSTANT REUSE AUDIT</div>
                {sel.id === "legacy" && (
                  <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="1/48" col={AMB}/><span style={{ fontSize:10, color:GRY }}>Charm's Zf — PSL(2,7) octahedral ✓</span></div>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="×1/3" col={RED}/><span style={{ fontSize:10, color:GRY }}>Stacked inversion — not independently derived ✗</span></div>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="= 1/144" col={RED}/><span style={{ fontSize:10, color:GRY }}>Effective free parameter ✗</span></div>
                  </div>
                )}
                {sel.id === "euler" && (
                  <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="e" col={GRN}/><span style={{ fontSize:10, color:GRY }}>Euler's number — already in m₀ = m_e/exp(2π/Φ) ✓</span></div>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="4" col={GRN}/><span style={{ fontSize:10, color:GRY }}>Spacetime dimension count — not fitted ✓</span></div>
                  </div>
                )}
                {sel.id === "phi8" && (
                  <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="κ=1/φ⁴" col={GRN}/><span style={{ fontSize:10, color:GRY }}>Superfluid bulk modulus — Theorem 1 Eq.(5) ✓</span></div>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="8" col={GRN}/><span style={{ fontSize:10, color:GRY }}>b = 8, the mod-8 base of Theorem 3 (8 = 2³)</span></div>
                    <div style={{ display:"flex", gap:8, alignItems:"center" }}><Tag label="κ/8" col={AMB}/><span style={{ fontSize:10, color:GRY }}>A selected combination: counted as a fitted Z_f (ledger §2.92)</span></div>
                  </div>
                )}
              </div>
            </div>
            <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"16px 18px" }}>
              <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:10 }}>NUMERICAL COMPARISON</div>
              {ZF_CANDIDATES.map(c => {
                const pred = mBase / c.Zf; const err = pct(pred, TOP_OBS); const ec = errColor(err);
                return (
                  <div key={c.id} style={{ marginBottom:10, opacity:c.id===selId?1:0.5 }}>
                    <div style={{ display:"flex", justifyContent:"space-between", marginBottom:3 }}>
                      <span style={{ fontFamily:MONO, fontSize:11, color:c.col }}>{c.label}</span>
                      <span style={{ fontFamily:MONO, fontSize:11, color:ec }}>{err>=0?"+":""}{err.toFixed(3)}%  {fmtMeV(pred)}</span>
                    </div>
                    <div style={{ height:4, background:DIM, borderRadius:2 }}>
                      <div style={{ width:`${Math.min(100, Math.abs(err)/3*100)}%`, height:"100%", background:ec, borderRadius:2 }}/>
                    </div>
                  </div>
                );
              })}
              <div style={{ marginTop:8, paddingTop:8, borderTop:`1px solid ${BRD}`, fontSize:10, color:GRY, fontFamily:MONO }}>Observed: 172,570 MeV (PDG 2024)</div>
            </div>
          </div>
        </div>
      )}

      {/* FULL TABLE */}
      {subtab === "table" && (
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"18px 20px" }}>
          <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:3, marginBottom:12 }}>FULL PARTICLE TABLE — TOP Zf = {sel.label}</div>
          <div style={{ overflowX:"auto" }}>
            <table style={{ width:"100%", borderCollapse:"collapse", fontFamily:MONO, fontSize:11 }}>
              <thead>
                <tr style={{ borderBottom:`1px solid ${BRD}` }}>
                  {["Gen","Particle","Zf","Predicted","Observed","Error","Status"].map(h => (
                    <th key={h} style={{ padding:"6px 10px", textAlign:"left", fontSize:9, color:GRY }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {PARTICLES.map((p, i) => {
                  const pred = p.id === "top" ? mBase / sel.Zf : mass(p.A, p.Zf, p.L);
                  const err  = pct(pred, p.obs); const ec = errColor(err);
                  const isTop = p.id === "top";
                  return (
                    <tr key={p.id} style={{ borderBottom:`1px solid ${DIM}`, background:isTop?`${sel.col}18`:i%2===0?"transparent":"#0d0d1a40" }}>
                      <td style={{ padding:"6px 10px" }}><Tag label={`G${p.gen}`} col={p.col}/></td>
                      <td style={{ padding:"6px 10px", color:p.col, fontWeight:isTop?700:400 }}>{p.label}{isTop?" ★":""}</td>
                      <td style={{ padding:"6px 10px", color:AMB }}>{isTop?sel.label:formatZf(p.Zf)}</td>
                      <td style={{ padding:"6px 10px", color:TXT }}>{fmtMeV(pred)}</td>
                      <td style={{ padding:"6px 10px", color:GRY }}>{fmtMeV(p.obs)}</td>
                      <td style={{ padding:"6px 10px" }}><span style={{ color:ec, fontWeight:700 }}>{err>=0?"+":""}{err.toFixed(3)}%</span></td>
                      <td style={{ padding:"6px 10px" }}><Tag label={Math.abs(err)<2?"PRECISION":Math.abs(err)<8?"GOOD":Math.abs(err)<20?"FRONTIER":"OPEN"} col={ec}/></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* EXPLORER */}
      {subtab === "explorer" && (
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"20px 24px" }}>
          <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:3, marginBottom:14 }}>CUSTOM Zf EXPLORER — FIND YOUR OWN CANDIDATE</div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
            <div>
              <div style={{ display:"flex", gap:8, marginBottom:16 }}>
                {[["phi","φ-series"],["e","e-series"],["manual","Manual"]].map(([id,lbl]) => (
                  <button key={id} onClick={() => setMode(id)} style={{ background:mode===id?DIM:"transparent", border:`1px solid ${mode===id?AMB:BRD}`, color:mode===id?AMB:GRY, padding:"5px 12px", borderRadius:3, fontFamily:MONO, fontSize:10, cursor:"pointer" }}>{lbl}</button>
                ))}
              </div>
              {mode === "phi" && (
                <div>
                  <Slider label="φ exponent" min={1} max={10} step={0.5} value={phiPow} onChange={setPhiPow} col={AMB}/>
                  <Slider label="Multiplier" min={1} max={24} step={1} value={phiMul} onChange={setPhiMul} col={AMB}/>
                  <div style={{ fontFamily:MONO, fontSize:10, color:GRY, lineHeight:1.8 }}>
                    Quick candidates:<br/>
                    {[[8,4],[1,4],[8,2],[3,4]].map(([m,po]) => {
                      const z = 1/(m*Math.pow(phi,po));
                      const er = pct(mBase/z, TOP_OBS);
                      return <span key={`${m}${po}`} style={{ display:"inline-block", marginRight:12, cursor:"pointer", color:Math.abs(er)<3?GRN:GRY }} onClick={() => { setPhiMul(m); setPhiPow(po); }}>1/({m}φ^{po}): <span style={{ color:errColor(er) }}>{er.toFixed(2)}%</span></span>;
                    })}
                  </div>
                </div>
              )}
              {mode === "e" && (
                <div>
                  <Slider label="Exponent n in e^(−n)" min={1} max={8} step={0.1} value={ePow} onChange={setEPow} col={CYA}/>
                  <div style={{ fontFamily:MONO, fontSize:10, color:GRY, lineHeight:1.8 }}>
                    Integer candidates:<br/>
                    {[2,3,4,5,6].map(n => {
                      const er = pct(mBase/Math.exp(-n), TOP_OBS);
                      return <span key={n} style={{ display:"inline-block", marginRight:12, cursor:"pointer" }} onClick={() => setEPow(n)}>e^−{n}: <span style={{ color:errColor(er) }}>{er.toFixed(2)}%</span></span>;
                    })}
                  </div>
                </div>
              )}
              {mode === "manual" && (
                <div>
                  <div style={{ fontSize:11, color:GRY, marginBottom:6 }}>Enter Zf directly</div>
                  <input type="number" value={manVal} step="0.0001" min="0.00001"
                    onChange={e => setManVal(Math.max(0.00001, parseFloat(e.target.value)||0.001))}
                    style={{ width:"100%", background:DIM, border:`1px solid ${BRD}`, color:TXT, fontFamily:MONO, fontSize:13, padding:"8px 12px", borderRadius:4 }}/>
                </div>
              )}
            </div>
            <div>
              <div style={{ background:DIM, border:`1px solid ${exEc}`, borderTop:`2px solid ${exEc}`, borderRadius:4, padding:"16px 18px", marginBottom:12 }}>
                <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:6 }}>LIVE RESULT — {exLabel}</div>
                <div style={{ fontFamily:MONO, fontSize:9, color:GRY, marginBottom:8 }}>Zf = {exZf.toFixed(8)} · 1/Zf = {(1/exZf).toFixed(4)}</div>
                <div style={{ fontFamily:MONO, fontSize:28, color:exEc, marginBottom:4 }}>{fmtMeV(exPred)}</div>
                <div style={{ fontFamily:MONO, fontSize:16, color:exEc }}>{exErr>=0?"+":""}{exErr.toFixed(4)}%</div>
              </div>
              <div style={{ background:DIM, borderRadius:4, padding:"12px 14px" }}>
                <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:1, marginBottom:6 }}>ERROR GAUGE (±5% window)</div>
                <div style={{ position:"relative", height:12, background:"#0a0a18", borderRadius:6, overflow:"hidden" }}>
                  <div style={{ position:"absolute", left:"50%", top:0, width:2, height:"100%", background:GRY, transform:"translateX(-1px)" }}/>
                  <div style={{ position:"absolute", left:exErr<0?`${Math.max(0,50+exErr/5*50)}%`:"50%", width:`${Math.min(50,Math.abs(exErr)/5*50)}%`, height:"100%", background:exEc, transition:"all 0.3s" }}/>
                </div>
                <div style={{ display:"flex", justifyContent:"space-between", fontSize:8, color:GRY, marginTop:3 }}>
                  <span>−5%</span><span>0 (perfect)</span><span>+5%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 16 — FINE-STRUCTURE CONSTANT
// ══════════════════════════════════════════════════════════════
function FineStructureTab() {
  const [rp, setRp]             = useState(RP_MUONIC);
  const [showSAaudit, setShowSAaudit] = useState(false);

  const pred = alphaInv(rp, 8 * Math.PI);
  const err  = pct(pred, ALPHA_OBS);
  const ec   = Math.abs(err) < 0.005 ? GRN : Math.abs(err) < 0.05 ? AMB : Math.abs(err) < 0.2 ? ORG : RED;
  const fc   = 1 + (rp * rp / (8 * Math.PI)) * kappa;

  const curveData = buildAlphaCurve();
  const W = 560, H = 220, PAD = { l:52, r:20, t:20, b:36 };
  const plotW = W - PAD.l - PAD.r, plotH = H - PAD.t - PAD.b;
  const rpMin = 0.820, rpMax = 0.890;
  const aMin = alphaInv(rpMin, 8*Math.PI), aMax = alphaInv(rpMax, 8*Math.PI);
  const xS = v => ((v - rpMin)/(rpMax - rpMin)) * plotW;
  const yS = a => plotH - ((a - aMin)/(aMax - aMin)) * plotH;
  const linePath = curveData.map((d,i) =>
    `${i===0?"M":"L"} ${(xS(d.rp)+PAD.l).toFixed(1)} ${(yS(d.alpha)+PAD.t).toFixed(1)}`
  ).join(" ");
  const markers = [
    { rp:RP_EXACT,  label:"Perfect match", col:GRN, offset:-14 },
    { rp:RP_MUONIC, label:"Muonic H",      col:CYA, offset:6   },
    { rp:RP_CODATA, label:"Old CODATA",    col:ORG, offset:6   },
  ].filter(m => m.rp >= rpMin && m.rp <= rpMax);

  return (
    <div style={{ color:TXT, fontFamily:"Georgia,serif" }}>
      <SectionHead col={CYA}>FINE-STRUCTURE CONSTANT · SOLID ANGLE RETRODICTION</SectionHead>

      {/* Epistemic status */}
      <div style={{ background:"#0a0a1a", border:`1px solid ${AMB}55`, borderLeft:`3px solid ${AMB}`,
        borderRadius:4, padding:"10px 16px", marginBottom:20, display:"flex", gap:14, alignItems:"flex-start" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:AMB, letterSpacing:2, whiteSpace:"nowrap", marginTop:2 }}>
          EPISTEMIC STATUS
        </div>
        <div style={{ fontSize:11, color:GRY, lineHeight:1.75 }}>
          This is a <strong style={{ color:AMB }}>high-precision retrodiction</strong>, not a theorem.
          r_p is taken from measurement; the formula then recovers α⁻¹ to 0.0028%.
          To become Theorem 4, the 8D manifold geometry must independently predict r_p = 0.83847 fm.
        </div>
      </div>

      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
        {/* Controls */}
        <div>
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"20px", marginBottom:14 }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:12 }}>INPUT — PROTON RADIUS r_p</div>
            <div style={{ marginBottom:12 }}>
              <div style={{ display:"flex", justifyContent:"space-between", marginBottom:5 }}>
                <span style={{ fontSize:11, color:GRY }}>r_p (fm)</span>
                <span style={{ fontFamily:MONO, fontSize:13, color:CYA }}>{rp.toFixed(5)} fm</span>
              </div>
              <input type="range" min={0.820} max={0.890} step={0.00001} value={rp}
                onChange={e => setRp(parseFloat(e.target.value))}
                style={{ width:"100%", accentColor:CYA, cursor:"pointer", height:4 }}/>
              <div style={{ display:"flex", justifyContent:"space-between", fontSize:8, color:GRY, marginTop:3 }}>
                <span>0.820</span><span>0.890 fm</span>
              </div>
            </div>
            <div style={{ display:"flex", flexDirection:"column", gap:7 }}>
              {[
                { rp:RP_EXACT,  label:"Perfect match",              val:"0.83847 fm", col:GRN, note:"Implied by α⁻¹ = 137.036 at 8π" },
                { rp:RP_MUONIC, label:"Muonic hydrogen (2018)",     val:"0.8414 fm",  col:CYA, note:"CODATA 2018 consensus" },
                { rp:RP_CODATA, label:"Electronic CODATA (legacy)", val:"0.8751 fm",  col:ORG, note:"Pre-muonic hydrogen value" },
              ].map(b => (
                <button key={b.rp} onClick={() => setRp(b.rp)} style={{
                  background: Math.abs(rp-b.rp)<0.00002 ? PNL : DIM,
                  border:`1px solid ${Math.abs(rp-b.rp)<0.00002 ? b.col : BRD}`,
                  borderRadius:4, padding:"8px 12px", cursor:"pointer",
                  display:"flex", justifyContent:"space-between", alignItems:"center" }}>
                  <div style={{ textAlign:"left" }}>
                    <div style={{ fontFamily:MONO, fontSize:10, color:b.col }}>{b.label}</div>
                    <div style={{ fontSize:9, color:GRY, marginTop:2 }}>{b.note}</div>
                  </div>
                  <span style={{ fontFamily:MONO, fontSize:11, color:b.col }}>{b.val}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Live output */}
          <div style={{ background:PNL, border:`1px solid ${ec}`, borderTop:`2px solid ${ec}`, borderRadius:6, padding:"16px 20px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:6 }}>PREDICTED α⁻¹</div>
            <div style={{ fontFamily:MONO, fontSize:32, color:ec, marginBottom:4 }}>{pred.toFixed(6)}</div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:8 }}>
              {[
                { l:"Error vs CODATA", v:`${err>=0?"+":""}${err.toFixed(4)}%`, c:ec },
                { l:"Correction fc",   v:fc.toFixed(8),                        c:AMB },
                { l:"Bare α⁻¹",        v:ALPHA_BARE.toFixed(4),                c:GRY },
              ].map(s => (
                <div key={s.l} style={{ background:DIM, borderRadius:3, padding:"8px 10px" }}>
                  <div style={{ fontSize:8, color:GRY, fontFamily:MONO, marginBottom:2 }}>{s.l}</div>
                  <div style={{ fontFamily:MONO, fontSize:12, color:s.c }}>{s.v}</div>
                </div>
              ))}
            </div>
            <div style={{ marginTop:10, fontFamily:MONO, fontSize:11, color:GRY, lineHeight:1.8 }}>
              α⁻¹ = {ALPHA_BARE} · (1 + r_p²·κ / 8π)
            </div>
          </div>
        </div>

        {/* SVG Chart */}
        <div>
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"16px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:8 }}>α⁻¹ vs r_p · SOLID ANGLE = 8π</div>
            <svg width={W} height={H} style={{ display:"block", maxWidth:"100%" }}>
              {[136.8, 137.0, 137.036, 137.2].map(a => {
                const y = yS(a) + PAD.t;
                if (y < PAD.t || y > H - PAD.b) return null;
                const isTarget = Math.abs(a - ALPHA_OBS) < 0.002;
                return (
                  <g key={a}>
                    <line x1={PAD.l} y1={y} x2={W-PAD.r} y2={y}
                      stroke={isTarget?`${GRN}66`:DIM} strokeWidth={isTarget?1.5:1}
                      strokeDasharray={isTarget?"0":"4 3"}/>
                    <text x={PAD.l-4} y={y+3} fill={isTarget?GRN:GRY}
                      fontSize="8" textAnchor="end">{a.toFixed(isTarget?3:1)}</text>
                  </g>
                );
              })}
              <path d={linePath} fill="none" stroke={CYA} strokeWidth="2" strokeLinecap="round"/>
              {markers.map(m => {
                const x = xS(m.rp)+PAD.l, y = yS(alphaInv(m.rp,8*Math.PI))+PAD.t;
                return (
                  <g key={m.rp}>
                    <line x1={x} y1={PAD.t} x2={x} y2={H-PAD.b}
                      stroke={m.col} strokeWidth="1.2" strokeDasharray="5 3" opacity="0.7"/>
                    <circle cx={x} cy={y} r="4" fill={BG} stroke={m.col} strokeWidth="2"/>
                    <text x={x+m.offset} y={PAD.t+12} fill={m.col} fontSize="8"
                      textAnchor={m.offset<0?"end":"start"}>{m.label}</text>
                    <text x={x+m.offset} y={PAD.t+22} fill={m.col} fontSize="7.5"
                      textAnchor={m.offset<0?"end":"start"}>{m.rp.toFixed(5)}</text>
                  </g>
                );
              })}
              {rp >= rpMin && rp <= rpMax && (() => {
                const x = xS(rp)+PAD.l, y = yS(pred)+PAD.t;
                return (
                  <g>
                    <line x1={x} y1={PAD.t} x2={x} y2={H-PAD.b} stroke={ec} strokeWidth="1.5" opacity="0.9"/>
                    <circle cx={x} cy={y} r="5" fill={ec} stroke={BG} strokeWidth="1.5"/>
                  </g>
                );
              })()}
              <line x1={PAD.l} y1={PAD.t} x2={PAD.l} y2={H-PAD.b} stroke={BRD} strokeWidth="1"/>
              <line x1={PAD.l} y1={H-PAD.b} x2={W-PAD.r} y2={H-PAD.b} stroke={BRD} strokeWidth="1"/>
              {[0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89].map(v => {
                const x = xS(v)+PAD.l;
                return (
                  <g key={v}>
                    <line x1={x} y1={H-PAD.b} x2={x} y2={H-PAD.b+4} stroke={GRY} strokeWidth="1"/>
                    <text x={x} y={H-PAD.b+14} fill={GRY} fontSize="8" textAnchor="middle">{v.toFixed(2)}</text>
                  </g>
                );
              })}
              <text x={W/2} y={H-2} fill={GRY} fontSize="8.5" textAnchor="middle">r_p (fm)</text>
              <text x={12} y={H/2} fill={GRY} fontSize="8.5" textAnchor="middle"
                transform={`rotate(-90 12 ${H/2})`}>α⁻¹</text>
            </svg>
          </div>
        </div>
      </div>

      {/* Solid angle uniqueness audit */}
      <div style={{ marginTop:20 }}>
        <button onClick={() => setShowSAaudit(s => !s)} style={{
          background:"transparent", border:`1px solid ${BRD}`, color:GRY,
          padding:"6px 14px", borderRadius:3, fontFamily:MONO, fontSize:9,
          cursor:"pointer", letterSpacing:1, marginBottom:10 }}>
          {showSAaudit ? "▼" : "▶"} SOLID ANGLE UNIQUENESS AUDIT
        </button>
        {showSAaudit && (
          <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"18px 20px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:2, marginBottom:12 }}>
              WHY 8π IS NOT ARBITRARY — SELECTION BY PHYSICAL CONSISTENCY
            </div>
            <div style={{ fontSize:11, color:GRY, lineHeight:1.75, marginBottom:16 }}>
              Three candidate solid angles correspond to distinct physical interpretations.
              Only 8π places the required r_p inside the measured proton radius range (0.83–0.88 fm).
            </div>
            <table style={{ width:"100%", borderCollapse:"collapse", fontFamily:MONO, fontSize:11 }}>
              <thead>
                <tr style={{ borderBottom:`1px solid ${BRD}` }}>
                  {["Solid Angle","Interpretation","Required r_p","Physical?","Status"].map(h => (
                    <th key={h} style={{ padding:"6px 12px", textAlign:"left", fontSize:9, color:GRY }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {SOLID_ANGLES.map(sa => (
                  <tr key={sa.label} style={{ borderBottom:`1px solid ${DIM}`, background:sa.label==="8π"?`${GRN}0a`:"transparent" }}>
                    <td style={{ padding:"8px 12px", color:sa.label==="8π"?GRN:GRY, fontWeight:sa.label==="8π"?700:400 }}>{sa.label}</td>
                    <td style={{ padding:"8px 12px", color:GRY, fontSize:10 }}>{sa.desc}</td>
                    <td style={{ padding:"8px 12px", color:sa.physical?TXT:RED, fontFamily:MONO }}>{sa.rp_req.toFixed(6)} fm</td>
                    <td style={{ padding:"8px 12px" }}><Tag label={sa.physical?"YES":"NO"} col={sa.physical?GRN:RED}/></td>
                    <td style={{ padding:"8px 12px" }}><Tag label={sa.label==="8π"?"SELECTED":"REJECTED"} col={sa.label==="8π"?GRN:GRY}/></td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ marginTop:14, background:DIM, borderRadius:4, padding:"12px 14px", borderLeft:`2px solid ${GRN}` }}>
              <div style={{ fontFamily:MONO, fontSize:9, color:GRN, letterSpacing:1, marginBottom:4 }}>IMPLICATION</div>
              <div style={{ fontSize:11, color:GRY, lineHeight:1.7 }}>
                The spin-½ double-cover interpretation is the unique solid angle choice that makes the
                formula physically self-consistent. This upgrades 8π from an assumption to a selection result.
                Remaining open step: deriving r_p = 0.83847 fm from 8D manifold geometry without experimental input.
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Open derivation */}
      <div style={{ marginTop:16, background:"#0a0014", border:`1px solid ${PRP}44`,
        borderLeft:`3px solid ${PRP}`, borderRadius:4, padding:"14px 18px" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:PRP, letterSpacing:2, marginBottom:6 }}>OPEN DERIVATION — PATH TO THEOREM 4</div>
        <div style={{ fontSize:11, color:GRY, lineHeight:1.75 }}>
          <strong style={{ color:TXT }}>1. Derive r_p from 8D geometry.</strong> The bulk-to-EM dimensional
          reduction must produce r_p = 0.83847 fm without experimental input.<br/><br/>
          <strong style={{ color:TXT }}>2. Close the coupled prediction.</strong> The same solid-angle integration
          closing the 0.41% α gap must also produce the proton radius — both emerging simultaneously from geometry.
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  TAB 17 — BARYON SECTOR (OPEN PROBLEM 5)
// ══════════════════════════════════════════════════════════════
function BaryonTab() {
  const [lSlider, setLSlider] = useState(L_B_BOUNDS.lo);   // start at the geometric length 58.006, not at the inversion
  const [showNeutron, setShowNeutron] = useState(false);

  const m_proton  = 938.272;
  const m_neutron = 939.565;
  const mPred     = mass(A_BORROMEAN, ZF_BORROMEAN, lSlider);
  const errP      = pct(mPred, m_proton);
  const errN      = pct(mPred, m_neutron);
  const ecP       = Math.abs(errP) < 0.05 ? GRN : Math.abs(errP) < 0.5 ? AMB : Math.abs(errP) < 2 ? ORG : RED;

  // Ropelength bar geometry
  const barMin = 55, barMax = 65;
  const barFrac = v => Math.max(0, Math.min(1, (v - barMin) / (barMax - barMin)));

  const sensitivityRows = [
    { L: L_B_BOUNDS.lo, src: "Ideal ropelength ≤ this (CFKSW 2006)" },
    { L: 58.0526,       src: "Four-arc configuration (CKS 2002)"    },
    { L: L_B_PREDICTED, src: "m_p inverted — not a prediction"      },
  ];

  return (
    <div style={{ color:TXT, fontFamily:"Georgia,serif" }}>
      <SectionHead col={RED}>BARYON SECTOR · BORROMEAN TOPOLOGY · ROPELENGTH PREDICTION FALSIFIED AT LEADING ORDER</SectionHead>

      {/* Status banner */}
      <div style={{ background:"#1a0a0a", border:`1px solid ${RED}55`, borderLeft:`3px solid ${RED}`,
        borderRadius:4, padding:"10px 16px", marginBottom:20, display:"flex", gap:14, alignItems:"flex-start" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:RED, letterSpacing:2, whiteSpace:"nowrap", marginTop:2 }}>
          EPISTEMIC STATUS
        </div>
        <div style={{ fontSize:11, color:GRY, lineHeight:1.75 }}>
          <strong style={{ color:RED }}>FALSIFIED AT LEADING ORDER (October 2026)</strong> — ledger §2.15 retracted to Conjecture (§2.92).
          The ideal Borromean ropelength is at most 58.006, the length of the presumed-minimal tight configuration
          (Cantarella, Fu, Kusner, Sullivan &amp; Wrinkle 2006), below the pre-stated window 60.194 ± 0.3; at 58.006 the formula
          gives about 759 MeV (−19%). L_B = 60.194 is the proton mass run backwards, so the proton and neutron matches are
          calibration outputs. A = 20 uses the diagonal Δ(t,t,t); the one-variable Alexander polynomial gives 70.
          Z_f = 6 remains Conjecture 1.
        </div>
      </div>

      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20, marginBottom:20 }}>

        {/* A = 20 panel */}
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderTop:`2px solid ${GRN}`, borderRadius:6, padding:"18px 20px" }}>
          <div style={{ fontFamily:MONO, fontSize:9, color:GRN, letterSpacing:2, marginBottom:10 }}>ALEXANDER INVARIANT · A = 20</div>
          <div style={{ fontFamily:MONO, fontSize:28, color:GRN, marginBottom:10 }}>A = 20</div>
          <div style={{ fontSize:11, color:GRY, lineHeight:1.8, marginBottom:14 }}>
            The proton is a Borromean link of three vortex strands (uud). The Borromean topology
            exactly mirrors color confinement: pairwise linking numbers are zero (no diquark
            confinement), yet the collective state is inseparable (color singlet).
          </div>
          <div style={{ background:DIM, borderRadius:4, padding:"12px 14px", fontFamily:MONO, fontSize:10, color:CYA, lineHeight:2 }}>
            Δ_B(t,t,t) = (t^½ − t^−½)³<br/>
            <span style={{ color:GRY }}>Coefficients: [1, −3, 3, −1]</span><br/>
            <span style={{ color:GRN }}>A = 1² + 3² + 3² + 1² = <strong>20</strong></span>
          </div>
          <div style={{ marginTop:12, padding:"8px 12px", background:`${GRN}12`, borderRadius:3, fontSize:10, color:GRY }}>
            Flavor-blind: A(proton) = A(neutron) = 20.
            Required for m_p ≈ m_n at leading order. ✓<br/>
            20 comes from the diagonal Δ(t,t,t); the one-variable Alexander polynomial, (t − 1)⁴, gives 70.
          </div>
        </div>

        {/* Z_f = 6 panel */}
        <div style={{ background:PNL, border:`1px solid ${BRD}`, borderTop:`2px solid ${PRP}`, borderRadius:6, padding:"18px 20px" }}>
          <div style={{ fontFamily:MONO, fontSize:9, color:PRP, letterSpacing:2, marginBottom:10 }}>PSL(2,7) STABILIZER · Z_f = 6</div>
          <div style={{ fontFamily:MONO, fontSize:28, color:PRP, marginBottom:10 }}>Z_f = 6</div>
          <div style={{ fontSize:11, color:GRY, lineHeight:1.8, marginBottom:14 }}>
            Three quarks in a color singlet occupy three non-collinear Fano points — a Fano triangle.
            Its stabilizer in PSL(2,7) ≅ GL(3,2) is S₃, of order 6, permuting the three points. Conjecture 1
            sets Z_f = |F₇*| = 6, the order of the multiplicative group of the Galois field F₇.
          </div>
          <div style={{ background:DIM, borderRadius:4, padding:"12px 14px", fontFamily:MONO, fontSize:10, color:PRP, lineHeight:2 }}>
            Stab(Fano triangle) ≅ S₃ ⊂ PSL(2,7), order 6<br/>
            <span style={{ color:GRY }}>F₇* ≅ Z₆ is not a subgroup of PSL(2,7): no element has order 6</span><br/>
            <span style={{ color:PRP }}>Z_f(baryon) = <strong>6</strong> (Conjecture 1)</span>
          </div>
          <div style={{ marginTop:12, display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:6 }}>
            {[
              { p:"Up",     zf:"3",  note:"Line stabilizer" },
              { p:"Down",   zf:"9",  note:"Amphicheiral (3²)" },
              { p:"Baryon", zf:"6",  note:"Conjecture 1", hi:true },
            ].map(r => (
              <div key={r.p} style={{ background:r.hi?`${PRP}18`:DIM, border:`1px solid ${r.hi?PRP:BRD}`, borderRadius:3, padding:"6px 8px", textAlign:"center" }}>
                <div style={{ fontFamily:MONO, fontSize:9, color:GRY }}>{r.p}</div>
                <div style={{ fontFamily:MONO, fontSize:14, color:r.hi?PRP:TXT }}>Z_f={r.zf}</div>
                <div style={{ fontSize:8, color:GRY, marginTop:2 }}>{r.note}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Ropelength prediction */}
      <div style={{ background:PNL, border:`1px solid ${BRD}`, borderRadius:6, padding:"18px 20px", marginBottom:20 }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:CYA, letterSpacing:2, marginBottom:14 }}>
          ROPELENGTH · INTERACTIVE EXPLORER · IDEAL LENGTH ≤ 58.006
        </div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:20 }}>
          <div>
            <Slider label="Borromean ropelength L_B (fm)" min={barMin} max={barMax} step={0.001}
              value={lSlider} onChange={setLSlider}
              display={`${lSlider.toFixed(3)} fm`} col={CYA}/>

            {/* Bounds bar */}
            <div style={{ position:"relative", height:32, marginBottom:14 }}>
              <div style={{ position:"absolute", left:0, right:0, top:12, height:8, background:DIM, borderRadius:4 }}/>
              {/* region allowed for the ideal ropelength: at most 58.006 */}
              <div style={{ position:"absolute",
                left:"0%",
                width:`${barFrac(L_B_BOUNDS.lo)*100}%`,
                top:12, height:8, background:`${GRN}33`, borderRadius:2 }}/>
              {/* the m_p-inverted length (60.194), outside the allowed region */}
              <div style={{ position:"absolute", left:`${barFrac(L_B_PREDICTED)*100}%`,
                top:6, width:2, height:20, background:RED, transform:"translateX(-1px)" }}/>
              {/* Slider cursor */}
              <div style={{ position:"absolute", left:`${barFrac(lSlider)*100}%`,
                top:8, width:3, height:16, background:ecP, borderRadius:2, transform:"translateX(-1px)", transition:"left 0.1s" }}/>
              <div style={{ position:"absolute", left:0, bottom:0, fontSize:8, color:GRY, fontFamily:MONO }}>{barMin}</div>
              <div style={{ position:"absolute", right:0, bottom:0, fontSize:8, color:GRY, fontFamily:MONO }}>{barMax}</div>
              <div style={{ position:"absolute", left:`${barFrac(L_B_BOUNDS.lo)*100}%`,
                bottom:0, fontSize:8, color:GRN, fontFamily:MONO }}>58.006</div>
              <div style={{ position:"absolute", left:`${barFrac(L_B_PREDICTED)*100}%`,
                bottom:0, fontSize:8, color:RED, fontFamily:MONO, transform:"translateX(-12px)" }}>60.194 (inverted)</div>
            </div>

            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8 }}>
              {[
                { l:"L_B solved from m_p", v:`${L_B_PREDICTED.toFixed(3)} fm`, c:RED },
                { l:"Slider ≤ 58.006 (ideal bound)?", v:lSlider<=L_B_BOUNDS.lo?"YES":"NO",
                  c:lSlider<=L_B_BOUNDS.lo?GRN:RED },
                { l:"m(A=20,Zf=6,L)",   v:`${mPred.toFixed(3)} MeV`, c:ecP },
                { l:"Error vs proton",  v:`${errP>=0?"+":""}${errP.toFixed(3)}%`, c:ecP },
              ].map(s => (
                <div key={s.l} style={{ background:DIM, borderRadius:3, padding:"8px 10px" }}>
                  <div style={{ fontSize:8, color:GRY, fontFamily:MONO, marginBottom:2 }}>{s.l}</div>
                  <div style={{ fontFamily:MONO, fontSize:12, color:s.c }}>{s.v}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Sensitivity table */}
          <div>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRY, letterSpacing:1, marginBottom:8 }}>MASS AT THE LENGTHS ON RECORD</div>
            <table style={{ width:"100%", borderCollapse:"collapse", fontFamily:MONO, fontSize:11 }}>
              <thead>
                <tr style={{ borderBottom:`1px solid ${BRD}` }}>
                  {["L (fm)","Source","m_pred","Error"].map(h => (
                    <th key={h} style={{ padding:"5px 8px", textAlign:"left", fontSize:9, color:GRY }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sensitivityRows.map(r => {
                  const mp = mass(A_BORROMEAN, ZF_BORROMEAN, r.L);
                  const ep = pct(mp, m_proton);
                  const ec2 = Math.abs(ep) < 0.05 ? GRN : Math.abs(ep) < 0.5 ? AMB : Math.abs(ep) < 2 ? ORG : RED;
                  const isMain = Math.abs(r.L - L_B_BOUNDS.lo) < 0.001;   // the geometric length, not the inversion
                  return (
                    <tr key={r.L} style={{ borderBottom:`1px solid ${DIM}`, background:isMain?`${GRN}0a`:"transparent" }}>
                      <td style={{ padding:"6px 8px", color:isMain?GRN:TXT, fontWeight:isMain?700:400 }}>{r.L.toFixed(3)}</td>
                      <td style={{ padding:"6px 8px", color:GRY, fontSize:9 }}>{r.src}</td>
                      <td style={{ padding:"6px 8px", color:TXT }}>{mp.toFixed(1)}</td>
                      <td style={{ padding:"6px 8px" }}>
                        <span style={{ color:ec2 }}>{ep>=0?"+":""}{ep.toFixed(3)}%</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Neutron test */}
      <div style={{ marginBottom:20 }}>
        <button onClick={() => setShowNeutron(s => !s)} style={{
          background:"transparent", border:`1px solid ${BRD}`, color:GRY,
          padding:"6px 14px", borderRadius:3, fontFamily:MONO, fontSize:9,
          cursor:"pointer", letterSpacing:1, marginBottom:10 }}>
          {showNeutron ? "▼" : "▶"} NEUTRON CHECK (CALIBRATION OUTPUT, NOT A TEST)
        </button>
        {showNeutron && (
          <div style={{ background:PNL, border:`1px solid ${GRN}`, borderRadius:6, padding:"18px 20px" }}>
            <div style={{ fontFamily:MONO, fontSize:9, color:GRN, letterSpacing:2, marginBottom:10 }}>
              NOT A TEST: L_B IS SOLVED FROM m_p, SO BOTH ROWS ARE CALIBRATION OUTPUTS
            </div>
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:12, marginBottom:14 }}>
              {[
                { l:"Proton (uud)",  obs:m_proton,  A:20, Zf:6, col:CYA },
                { l:"Neutron (udd)", obs:m_neutron, A:20, Zf:6, col:AMB },
              ].map(r => {
                const mp = mass(r.A, r.Zf, L_B_PREDICTED);
                const ep = pct(mp, r.obs);
                return (
                  <div key={r.l} style={{ background:DIM, borderRadius:4, padding:"12px 14px" }}>
                    <div style={{ fontFamily:MONO, fontSize:9, color:r.col, marginBottom:4 }}>{r.l}</div>
                    <div style={{ fontFamily:MONO, fontSize:9, color:GRY }}>A={r.A} · Z_f={r.Zf} · L={L_B_PREDICTED.toFixed(3)}</div>
                    <div style={{ fontFamily:MONO, fontSize:18, color:GRN, margin:"6px 0" }}>{mp.toFixed(3)} MeV</div>
                    <div style={{ fontSize:9, color:GRY }}>obs {r.obs} MeV · err <span style={{ color:Math.abs(ep)<0.2?GRN:AMB }}>{ep>=0?"+":""}{ep.toFixed(4)}%</span></div>
                  </div>
                );
              })}
              {/* QED floor panel — computes errP and errN at L_B_PREDICTED and makes the hadronic/EM split explicit */}
              <div style={{ background:`${GRN}12`, border:`1px solid ${GRN}44`, borderRadius:4, padding:"12px 14px" }}>
                <div style={{ fontFamily:MONO, fontSize:9, color:GRN, marginBottom:8 }}>n-p SPLIT · QED FLOOR</div>
                {(() => {
                  const mHad = mass(A_BORROMEAN, ZF_BORROMEAN, L_B_PREDICTED);
                  const epP  = pct(mHad, m_proton);
                  const epN  = pct(mHad, m_neutron);
                  return (
                    <>
                      <div style={{ fontFamily:MONO, fontSize:13, color:CYA, marginBottom:8 }}>
                        Δm = {(m_neutron - m_proton).toFixed(3)} MeV
                      </div>
                      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:4, marginBottom:10 }}>
                        <div style={{ fontSize:9, color:GRY }}>
                          p err: <span style={{ color:Math.abs(epP)<0.2?GRN:AMB }}>{epP>=0?"+":""}{epP.toFixed(4)}%</span>
                        </div>
                        <div style={{ fontSize:9, color:GRY }}>
                          n err: <span style={{ color:Math.abs(epN)<0.2?GRN:AMB }}>{epN>=0?"+":""}{epN.toFixed(4)}%</span>
                        </div>
                      </div>
                      <div style={{ fontSize:10, color:GRY, lineHeight:1.65 }}>
                        Δm is electromagnetic in origin (QED). Theorem 1 gives hadronic mass only — p and n share identical topology.
                        <br/><br/>
                        <strong style={{ color:GRY }}>Topology-blind Borromean: p and n identical by construction</strong>
                      </div>
                    </>
                  );
                })()}
              </div>
            </div>
            <div style={{ fontSize:10, color:GRY, lineHeight:1.7 }}>
              Earlier prescriptions (A=99, A=363, A=20 with Z_f=φ/6) are on record. With A = 20 and Z_f = 6 the length
              is solved from m_p, so the match is by construction; at the geometric length 58.006 the formula gives about 759 MeV.
            </div>
          </div>
        )}
      </div>

      {/* Open items */}
      <div style={{ background:"#0a0014", border:`1px solid ${PRP}44`, borderLeft:`3px solid ${PRP}`,
        borderRadius:4, padding:"14px 18px" }}>
        <div style={{ fontFamily:MONO, fontSize:9, color:PRP, letterSpacing:2, marginBottom:8 }}>
          PAPER VII ITEMS
        </div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, fontSize:11, color:GRY, lineHeight:1.75 }}>
          <div>
            <strong style={{ color:TXT }}>Appendix E.1 — resolved negative (October 2026).</strong> The ideal Borromean
            ropelength is at most 58.006 (CFKSW 2006), outside the window 60.194 ± 0.3: the ropelength prediction is
            falsified at leading order (ledger §2.15 retracted to Conjecture, §2.92).
          </div>
          <div>
            <strong style={{ color:TXT }}>Conjecture 1 (formal proof).</strong> Riemann-Hurwitz derivation
            of Z_f = 6 from the branched covering of the Borromean complement. Must show the fundamental
            group representation factors through F₇*. Currently motivated but not complete.
          </div>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
//  MAIN APP
// ══════════════════════════════════════════════════════════════
export default function SQT180() {
  const [tab, setTab]         = useState("audit");
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setTimeout(() => setMounted(true), 40); }, []);

  const TABS = [
    { id:"audit",    label:"Mass Audit",    col:"#e2e2e2" },
    { id:"calc",     label:"Calculator",    col:AMB },
    { id:"spectrum", label:"Spectrum",      col:GRN },
    { id:"worticity",label:"Worticity",     col:PRP },
    { id:"gen1",     label:"Gen I",         col:GRN },
    { id:"gen2",     label:"Gen II",        col:ORG },
    { id:"gen3",     label:"Gen III",       col:RED },
    { id:"leptons",  label:"Leptons",       col:"#818cf8" },
    { id:"force",    label:"Force-Residual",col:RED },
    { id:"neutrino", label:"Neutrinos",     col:"#38bdf8" },
    { id:"weak",     label:"Weak Bosons",   col:PRP },
    { id:"finestr",  label:"Fine Structure", col:CYA },
    { id:"baryon",   label:"Baryon ★",       col:RED },
    { id:"lens",     label:"Lens Eq",        col:ORG },
    { id:"echoes",   label:"Cosmic Echoes",  col:CYA },
    { id:"freeze",   label:"Freeze-Out",     col:AMB },
    { id:"topzf",    label:"Top Zf ★",       col:PRP },
  ];

  const hdr = [
    { l:"Top",    v:pct(mass(119,1/(8*phi4),37.31),172570), fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },
    { l:"Bottom", v:pct(mass(119,0.75,37.31),4183),         fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },
    { l:"Tau",    v:pct(mass(3,ZF_LEPTON,3*L_q),1776.93),fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },
    { l:"Muon",   v:pct(mass(1,ZF_LEPTON,2*L_q),105.658),fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },
    { l:"W (retired)", v:pct(m0*Math.pow(phi,27),80369.2),   fmt:v=>`${v>=0?"+":""}${v.toFixed(2)}%` },
    { l:"ν",      v:null, fmt:()=>`${(m0/Math.pow(XI_VAC,3)*1e6).toFixed(4)} eV` },
    { l:"α⁻¹",   v:pct(alphaInv(RP_MUONIC,8*Math.PI),ALPHA_OBS), fmt:v=>`${v>=0?"+":""}${v.toFixed(4)}%` },
    { l:"L_B (inverted)", v:null, fmt:()=>`${L_B_PREDICTED.toFixed(3)} fm` },
  ];

  return (
    <div style={{ minHeight:"100vh", background:BG, color:TXT, fontFamily:"Georgia,serif", opacity:mounted?1:0, transition:"opacity 0.4s" }}>

      {/* Header */}
      <div style={{ padding:"16px 28px 14px", borderBottom:`1px solid ${BRD}`, background:"#09090f" }}>
        <div style={{ fontFamily:MONO, fontSize:8, color:"#3a3a6a", letterSpacing:4, marginBottom:4 }}>
          SQT · v1.9.1 DRAFT · Matthew Gifford · Ridgemark CA · April 2026 · status corrections October 2026
        </div>
        <h1 style={{ margin:"0 0 4px", fontSize:20, fontWeight:400, letterSpacing:-0.3 }}>
          Superfluid Quantum Topology — Leading-Order Mass Fit
        </h1>
        <div style={{ fontSize:10, color:GRY, marginBottom:12 }}>
          Φ={PHI.toFixed(6)} · m₀={m0.toFixed(5)} MeV · κ=1/φ⁴≈{kappa.toFixed(4)} · ξvac=100φ≈{XI_VAC.toFixed(2)} · Lepton Zf=1/2π · Top Zf=1/(8φ⁴) · one anchor (m_e), one selected scale (ξvac), Z_f and L selected per particle
        </div>
        <div style={{ display:"grid", gridTemplateColumns:"repeat(8,1fr)", gap:8 }}>
          {hdr.map(s => (
            <div key={s.l} style={{ background:PNL, border:`1px solid ${errColor(s.v??0)}33`, borderTop:`2px solid ${errColor(s.v??0)}`, borderRadius:4, padding:"7px 12px" }}>
              <div style={{ fontSize:9, color:GRY, fontFamily:MONO, marginBottom:2 }}>{s.l}</div>
              <div style={{ fontFamily:MONO, fontSize:13, color:errColor(s.v??0) }}>{s.fmt(s.v)}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Tab bar */}
      <div style={{ display:"flex", borderBottom:`1px solid ${BRD}`, padding:"0 28px", background:"#09090f", overflowX:"auto" }}>
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{ background:"transparent", border:"none", borderBottom:tab===t.id?`2px solid ${t.col}`:"2px solid transparent", color:tab===t.id?t.col:GRY, padding:"10px 14px", fontSize:10, fontFamily:MONO, cursor:"pointer", letterSpacing:1, whiteSpace:"nowrap" }}>
            {t.label.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ padding:"22px 28px 48px" }}>
        {tab === "audit"     && <MassAudit />}
        {tab === "calc"      && <MassCalc />}
        {tab === "spectrum"  && <SpectrumChart />}
        {tab === "worticity" && <Worticity />}
        {tab === "gen1"      && <GenIKnotMap />}
        {tab === "gen2"      && <GenIIKnotMap />}
        {tab === "gen3"      && <GenIIIKnotMap />}
        {tab === "leptons"   && <LeptonKnotMap />}
        {tab === "force"     && <ForceResidual />}
        {tab === "neutrino"  && <NeutrinoSector />}
        {tab === "weak"      && <ElectroweakSector />}
        {tab === "lens"      && <LensEquation />}
        {tab === "echoes"    && <CosmologicalEchoes />}
        {tab === "freeze"    && <ThermodynamicFreezeOut />}
        {tab === "topzf"     && <TopZfTab />}
        {tab === "finestr"   && <FineStructureTab />}
        {tab === "baryon"    && <BaryonTab />}
      </div>

      {/* Footer */}
      <div style={{ borderTop:`1px solid ${BRD}`, padding:"8px 28px", display:"flex", justifyContent:"space-between", fontSize:8, fontFamily:MONO, color:"#252540" }}>
        <span>SQT v1.9.1 DRAFT (October 2026 status corrections) · Matthew Gifford · Ridgemark CA · Collaborative synthesis with Gemini (Google AI) and Claude (Anthropic)</span>
        <span>m=m₀·(A/Zf)·exp(L/Φreff) · Lepton Zf=1/2π · ν:Zf=ξvac³ · W:m₀·φ²⁷ (retired) · α⁻¹:bare·(1+r_p²κ/8π) · L_B={L_B_PREDICTED.toFixed(3)} (m_p inverted)</span>
      </div>

      <style>{`
        * { box-sizing: border-box; margin: 0; padding: 0; }
        button:focus { outline: none; }
        input[type=range] { height: 4px; border-radius: 2px; }
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: #07070f; }
        ::-webkit-scrollbar-thumb { background: #1a1a30; border-radius: 3px; }
      `}</style>
    </div>
  );
}
