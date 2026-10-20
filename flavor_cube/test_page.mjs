// Tests for the logic inside index.html, run in Node without a browser:  node flavor_cube/test_page.mjs
// It evaluates the page's <script id="pure"> and <script id="presets-data"> blocks and checks them against
// group theory, the Rubik's group, E4's stored chi2 values, and (when present) geometry.json and mixing.json.
import fs from 'node:fs';
import vm from 'node:vm';

const here = new URL('.', import.meta.url);
const html = fs.readFileSync(new URL('index.html', here), 'utf8');
const block = (id) => {
  const m = html.match(new RegExp('<script id="' + id + '">([\\s\\S]*?)</script>'));
  if (!m) throw new Error('missing script block ' + id);
  return m[1];
};
const ctx = { module: {}, console, Math };
vm.createContext(ctx);
vm.runInContext(block('pure') + '\n;globalThis.Pure = Pure;', ctx);
vm.runInContext(block('presets-data') + '\n;globalThis.PRESETS = PRESETS;', ctx);
const P = ctx.Pure, PRESETS = ctx.PRESETS;

let fails = 0, passes = 0;
function check(name, ok, detail) {
  if (ok) { passes++; console.log('PASS', name); }
  else { fails++; console.log('FAIL', name, detail === undefined ? '' : detail); }
}
const close = (a, b, tol) => Math.abs(a - b) <= tol * Math.max(1, Math.abs(a), Math.abs(b));
const key = (M) => JSON.stringify(M);

// ---------------------------------------------------------------- geometry
const G = P.stabilizer();
check('stabilizer of v0 in Aut(Fano+) has 24 elements', G.length === 24, G.length);
const counts = {};
for (const g of G) counts[g.cls] = (counts[g.cls] || 0) + 1;
check('classes E:1 C3:8 C2:3 S4:6 sigma_d:6', counts.E === 1 && counts.C3 === 8 && counts.C2 === 3 && counts.S4 === 6 && counts.sigma_d === 6, JSON.stringify(counts));

// T_d = signed permutation matrices D*Perm with det D = +1
const Td = new Set();
const perms3 = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
for (const p of perms3) for (const s of [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) {
  const M = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let i = 0; i < 3; i++) M[i][p[i]] = s[i];
  Td.add(key(M));
}
const mats = new Set(G.map((g) => key(g.matrix)));
check('{P_g} is exactly T_d (24 distinct matrices)', mats.size === 24 && [...mats].every((m) => Td.has(m)));
check('no 90-degree rotation and no inversion among P_g', G.every((g) => g.cls !== 'C4' && g.cls !== 'i'));
let closed = true;
for (const a of G) for (const b of G) if (!mats.has(key(P.mul(a.matrix, b.matrix)))) closed = false;
check('P_g closed under multiplication', closed);
// homomorphism: P_{g h} = P_g P_h with (g h)(x) = g(h(x))
let hom = true;
for (const a of G) for (const b of G) {
  const gh = a.g.map((_, x) => a.g[b.g[x]]);
  if (key(P.faceMatrix(gh)) !== key(P.mul(a.matrix, b.matrix))) hom = false;
}
check('g -> P_g is a homomorphism', hom);
const tor = G.filter((g) => g.torus).map((g) => g.torus).sort();
check('torus rotations in the stabilizer are exactly id, x->2x, x->4x', JSON.stringify(tor) === JSON.stringify(['id', 'x->2x', 'x->4x']), tor);
const two = G.find((g) => g.torus === 'x->2x');
check('x->2x is the 120 degree turn about (1,1,1)', two.cls === 'C3' && key(two.axis) === key([1, 1, 1]) && two.angle === 120, JSON.stringify(two));
for (const a of [3, 5, 6]) {
  const g = [0, 1, 2, 3, 4, 5, 6].map((x) => P.mod7(a * x));
  check('x->' + a + 'x is not a Fano+ collineation', !P.isPlusCollineation(g));
}
const C8 = P.corners();
const t1 = C8.filter((c) => c.tetra === 'T1'), t2 = C8.filter((c) => c.tetra === 'T2');
check('the four T1 corners are exactly the Fano+ lines missing 0', t1.every((c) => c.plus) && t2.every((c) => !c.plus));
check('(-,-,-) = {3,5,6} is a Fano- line; the other T2 corners are lines of neither plane',
  t2.filter((c) => c.minus).length === 1 && key(t2.find((c) => c.minus).faces) === key([3, 5, 6]));
check('QR corner fixed by exactly 6 elements (S3)', G.filter((g) => g.fixesQRCorner).length === 6);
// pairings
const isPair = (M, a, b) => M.some(([x, y]) => (x === a && y === b) || (x === b && y === a));
const opp = (a, b) => P.NORMAL[a].every((v, i) => v === -P.NORMAL[b][i]);
check('J3 pairs are opposite faces', P.PAIRINGS.J3.every(([a, b]) => opp(a, b)));
check('J5 and J6 pairs are adjacent faces', [...P.PAIRINGS.J5, ...P.PAIRINGS.J6].every(([a, b]) => !opp(a, b) && a !== b));
check('J_c pairs are (r, c r mod 7)', ['J3', 'J5', 'J6'].every((J) => P.PAIRINGS[J].every(([r, s]) => s === P.mod7(Number(J.slice(1)) * r) && P.QR.includes(r))));
// hexagons: link alternates J3/J5, corner view alternates J5/J6
const alt = (order, A, B) => order.every((a, k) => { const b = order[(k + 1) % 6]; return (k % 2 === 0 ? isPair(P.PAIRINGS[A], a, b) : isPair(P.PAIRINGS[B], a, b)); });
check('torus link order alternates J3, J5 and has J6 opposite', alt(P.LINK_ORDER, 'J3', 'J5') && P.PAIRINGS.J6.every(([a, b]) => Math.abs(P.LINK_ORDER.indexOf(a) - P.LINK_ORDER.indexOf(b)) === 3));
check('corner-view order alternates J5, J6 and has J3 opposite', alt(P.CORNER_VIEW_ORDER, 'J5', 'J6') && P.PAIRINGS.J3.every(([a, b]) => Math.abs(P.CORNER_VIEW_ORDER.indexOf(a) - P.CORNER_VIEW_ORDER.indexOf(b)) === 3));
// corner view really is the projection order along (1,1,1)
const proj = (a) => { const n = P.NORMAL[a]; const u = [1 / Math.sqrt(2), -1 / Math.sqrt(2), 0], w = [1 / Math.sqrt(6), 1 / Math.sqrt(6), -2 / Math.sqrt(6)]; return Math.atan2(n[0] * w[0] + n[1] * w[1] + n[2] * w[2], n[0] * u[0] + n[1] * u[1] + n[2] * u[2]); };
const byAngle = [1, 2, 3, 4, 5, 6].sort((a, b) => proj(a) - proj(b));
const rotEq = (x, y) => { for (let s = 0; s < 6; s++) { if (x.every((v, i) => v === y[(i + s) % 6])) return true; const r = y.slice().reverse(); if (x.every((v, i) => v === r[(i + s) % 6])) return true; } return false; };
check('projection along (1,1,1) puts the faces in the corner-view order', rotEq(byAngle, P.CORNER_VIEW_ORDER), byAngle);
// Fano diagram used by the inset: sides, medians and circle are the Fano+ lines
const diagram = [[3, 5, 2], [3, 6, 4], [5, 6, 1], [3, 0, 1], [6, 0, 2], [5, 0, 4], [1, 2, 4]].map((t) => key(t.slice().sort((a, b) => a - b)));
check('inset Fano diagram lines are exactly the Fano+ lines', new Set(diagram).size === 7 && P.FANO_PLUS.every((L) => diagram.includes(key(L))));

// ---------------------------------------------------------------- puzzle
let seed = 12345;
const rnd = (n) => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed % n; };
const toks = ['U', 'D', 'R', 'L', 'F', 'B'].flatMap((f) => [f, f + "'"]);
let inv = true, solves = true, twistOk = true;
for (let trial = 0; trial < 1500; trial++) {
  const c = P.newCube(), seq = [];
  const n = 1 + rnd(40);
  for (let i = 0; i < n; i++) { const t = toks[rnd(12)]; seq.push(t); P.applyMove(c, t); if (P.twistTotal(c) !== 0) inv = false; }
  for (let i = seq.length - 1; i >= 0; i--) P.applyMove(c, P.inverseToken(seq[i]));
  if (!P.isSolved(c)) solves = false;
  const d = P.newCube();
  for (let i = 0; i < n; i++) P.applyMove(d, toks[rnd(12)]);
  const corner = d.cubies.filter((k) => k.home.every((v) => v !== 0))[rnd(8)].pos;
  P.twistCorner(d, corner, rnd(2) ? 1 : -1);
  const tt = P.twistTotal(d);
  if (tt === 0) twistOk = false;
  for (let i = 0; i < 30; i++) P.applyMove(d, toks[rnd(12)]);
  if (P.twistTotal(d) !== tt) twistOk = false;
}
check('legal turns keep total corner twist 0 mod 3 (1500 random sequences)', inv);
check('playing a sequence backwards solves the cube', solves);
check('one hand twist makes the total 1 or 2, and legal turns keep it', twistOk);
const order = (seq) => { const c = P.newCube(); for (let k = 1; k <= 2000; k++) { for (const t of seq) P.applyMove(c, t); if (P.isSolved(c)) return k; } return -1; };
check("order of R U R' U' is 6", order(['R', 'U', "R'", "U'"]) === 6);
check('order of R U is 105', order(['R', 'U']) === 105);
check('order of each face turn is 4', ['U', 'D', 'R', 'L', 'F', 'B'].every((t) => order([t]) === 4));
// U is clockwise seen from above: the front-right-top corner goes to the front-left... check UFR -> UFL
{
  const c = P.newCube(); const cub = c.cubies.find((k) => key(k.pos) === key([1, 1, 1]));
  P.applyMove(c, 'U');
  check('U (clockwise from above) sends the UFR corner to UFL', key(cub.pos) === key([-1, 1, 1]), cub.pos);
  const d = P.newCube(); const e = d.cubies.find((k) => key(k.pos) === key([1, 1, 1]));
  P.applyMove(d, 'R');
  check('R (clockwise from the right) sends the UFR corner to UBR', key(e.pos) === key([1, 1, -1]), e.pos);
}

// ---------------------------------------------------------------- mixing
function anglesOf(p) {
  if (p.wolf) return P.anglesFromWolfenstein(p.wolf[0], p.wolf[1], p.wolf[2], p.wolf[3]);
  return { t12: Math.asin(Math.sqrt(p.s12sq)), t13: Math.asin(Math.sqrt(p.s13sq)), t23: Math.asin(Math.sqrt(p.s23sq)), d: (p.d === null ? 0 : p.d) * P.RAD, dDef: p.d !== null };
}
function chi2Of(sector, p) {
  const a = anglesOf(p);
  const U = P.pdgU(a.t12, a.t13, a.t23, a.d);
  if (sector === 'quark') return { r: P.chi2Ckm(U), U };
  const s = (t) => Math.pow(Math.sin(t), 2);
  return { r: P.chi2Pmns(s(a.t12), s(a.t13), s(a.t23), a.dDef === false ? null : a.d / P.RAD), U };
}
const L = Object.fromEntries(PRESETS.lepton.map((p) => [p.id, p])), Q = Object.fromEntries(PRESETS.quark.map((p) => [p.id, p]));
const pyJSON = (txt) => JSON.parse(txt.replace(/\bNaN\b/g, 'null').replace(/-?\bInfinity\b/g, 'null'));   // Python's json writes NaN
const e4 = pyJSON(fs.readFileSync(new URL('../seed/experiments/E4_family_symmetry/results.json', here), 'utf8'));
const z2 = e4.z2_partial_PSL.filter((x) => x['survives(p>0.01)']);
const refs = {
  e4_z7: z2.find((x) => x.G_l === 'Z7').chi2,
  e4_tm1: z2.find((x) => x.G_l === 'Z3' && Math.abs(Math.max(...x.fixed_column_abs2) - 2 / 3) < 1e-4).chi2,
  e4_tm2: z2.find((x) => x.G_l === 'Z3' && Math.abs(Math.max(...x.fixed_column_abs2) - 1 / 3) < 1e-4).chi2,
};
for (const [id, ref] of Object.entries(refs)) {
  const c = chi2Of('lepton', L[id]).r.chi2;
  check('chi2 of ' + id + ' reproduces E4 (' + ref.toFixed(4) + ')', close(c, ref, 1e-9), c);
}
check('NuFIT preset has chi2 0', close(chi2Of('lepton', L.pmns_nufit).r.chi2, 0, 1e-12));
const none = chi2Of('lepton', L.none).r.chi2;
check('no mixing gives E4\'s best F21 lepton chi2 (2459.1)', Math.abs(none - 2459.1) < 0.1, none);
const tbm = chi2Of('lepton', L.tbm);
const A2 = P.absSq(tbm.U);
check('tri-bimaximal: middle column is (1/3, 1/3, 1/3)', A2.every((r) => close(r[1], 1 / 3, 1e-12)));
check('tri-bimaximal: first column is (2/3, 1/6, 1/6)', close(A2[0][0], 2 / 3, 1e-12) && close(A2[1][0], 1 / 6, 1e-12) && close(A2[2][0], 1 / 6, 1e-12));
const tm2 = P.absSq(chi2Of('lepton', L.e4_tm2).U);
check('TM2 preset keeps the middle column trimaximal', tm2.every((r) => close(r[1], 1 / 3, 1e-5)), tm2.map((r) => r[1]));
const tm1 = P.absSq(chi2Of('lepton', L.e4_tm1).U);
check('TM1 preset keeps the first column (2/3, 1/6, 1/6)', close(tm1[0][0], 2 / 3, 1e-5) && close(tm1[1][0], 1 / 6, 1e-5) && close(tm1[2][0], 1 / 6, 1e-5), tm1.map((r) => r[0]));
check('UTfit preset round-trips (chi2 0)', close(chi2Of('quark', Q.ckm_utfit).r.chi2, 0, 1e-12) || chi2Of('quark', Q.ckm_utfit).r.chi2 < 1e-16);
const sinPull = chi2Of('quark', Q.ckm_sin_3_13).r.pulls;
check('sin 3/13: only lambda pulls, by (3/13 - 0.22519)/0.00083', close(sinPull.lambda, (3 / 13 - 0.22519) / 0.00083, 1e-9) && Math.abs(sinPull.A) < 1e-8 && Math.abs(sinPull.rhobar) < 1e-8 && Math.abs(sinPull.etabar) < 1e-8, JSON.stringify(sinPull));
check('3/13 vs PDG 2024 |V_us| 0.22431(85) is 7.6 sigma', Math.abs((3 / 13 - 0.22431) / 0.00085 - 7.6) < 0.05);
check('3/13 vs PDG 2024 global lambda 0.22501(68) is 8.5 sigma', Math.abs((3 / 13 - 0.22501) / 0.00068 - 8.47) < 0.05);
const tanA = anglesOf(Q.ckm_tan_3_13);
check('tan preset has tan theta12 = 3/13', close(Math.tan(tanA.t12), 3 / 13, 1e-12));
check('no-mixing CKM has no chi2 (A undefined)', !chi2Of('quark', Q.none).r.defined);
// cube rotation: exact for delta = 0 or 180
{
  const a = anglesOf(L.pmns_nufit);
  const r = P.cubeRotation(a.t12, a.t13, a.t23, Math.PI);
  const U = P.pdgU(a.t12, a.t13, a.t23, Math.PI);
  check('with delta = 180 the cube rotation equals the real PDG matrix', r.O.every((row, i) => row.every((x, j) => Math.abs(x - U[i][j][0]) < 1e-12 && Math.abs(U[i][j][1]) < 1e-12)));
  const O = P.cubeRotation(a.t12, a.t13, a.t23, 0.3).O;
  check('cube rotation is orthogonal with det +1', Math.abs(P.det(O) - 1) < 1e-12 && P.mul(O, P.transpose(O)).every((row, i) => row.every((x, j) => Math.abs(x - (i === j ? 1 : 0)) < 1e-12)));
}

// ---------------------------------------------------------------- cross-check against the Python outputs, when present
function maybe(name) { try { return pyJSON(fs.readFileSync(new URL(name, here), 'utf8')); } catch (e) { return null; } }
const geo = maybe('geometry.json');
if (geo) {
  const pyMats = new Set(geo.stabilizer.map((e) => key(e.matrix)));
  check('geometry.json stabilizer matrices equal the page\'s', pyMats.size === 24 && [...pyMats].every((m) => mats.has(m)));
  const pyCls = {}; for (const e of geo.stabilizer) pyCls[key(e.matrix)] = e.class;
  check('geometry.json classes equal the page\'s', G.every((g) => pyCls[key(g.matrix)] === g.cls), G.filter((g) => pyCls[key(g.matrix)] !== g.cls).map((g) => [g.cls, pyCls[key(g.matrix)]]));
  check('geometry.json corner-view order matches', rotEq(geo.corner_view_order, P.CORNER_VIEW_ORDER));
  check('geometry.json link order matches', rotEq(geo.link_order, P.LINK_ORDER));
} else console.log('SKIP geometry.json not found');
const mix = maybe('mixing.json');
if (mix) {
  for (const pr of mix.presets) {
    const sector = pr.id.startsWith('ckm') ? 'quark' : (pr.id === 'none' ? null : 'lepton');
    const list = sector === 'quark' ? Q : L;
    const p = list[pr.id];
    if (!p) { console.log('SKIP mixing.json preset not on page:', pr.id); continue; }
    const { r, U } = chi2Of(sector, p);
    const A = P.absSq(U);
    const okU = pr.absU2.every((row, i) => row.every((x, j) => Math.abs(x - A[i][j]) < 1e-9));
    const okC = pr.chi2 === null ? !Number.isFinite(r.chi2) : close(r.chi2, pr.chi2, 1e-7);
    check('mixing.json ' + pr.id + ': |U|^2 and chi2 match the page', okU && okC, { page: r.chi2, py: pr.chi2 });
    const a = anglesOf(p), cr = P.cubeRotation(a.t12, a.t13, a.t23, a.d);
    check('mixing.json ' + pr.id + ': cube delta matches', cr.cubeDeltaDeg === pr.cube_delta_deg, [cr.cubeDeltaDeg, pr.cube_delta_deg]);
  }
} else console.log('SKIP mixing.json not found');

console.log(`\n${passes} passed, ${fails} failed`);
process.exit(fails ? 1 : 0);
