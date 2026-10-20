// Browser smoke test for index.html:  node flavor_cube/test_browser.mjs [--three path/to/three.min.js] [--shots dir]
// Loads the page in headless Chromium, clicks through every mode, and fails on console errors,
// horizontal page overflow, or state that does not match the page's own logic.
// --three serves a local copy of three.js r128 in place of cdnjs (for sandboxes without network).
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const threePath = opt('--three');
const shots = opt('--shots');
if (shots) fs.mkdirSync(shots, { recursive: true });

let chromium;
try { ({ chromium } = await import('playwright')); }
catch (e) { ({ chromium } = createRequire(path.join(path.dirname(process.execPath), '../lib/node_modules/'))('playwright')); }

const here = path.dirname(new URL(import.meta.url).pathname);
const pageUrl = 'file://' + path.join(here, 'index.html');
const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
let fails = 0;
const check = (name, ok, detail) => { console.log((ok ? 'PASS ' : 'FAIL ') + name + (ok || detail === undefined ? '' : ' ' + JSON.stringify(detail))); if (!ok) fails++; };

async function open(viewport, scheme) {
  const ctx = await browser.newContext({ viewport, colorScheme: scheme, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/fonts\.g(oogleapis|static)\.com|ERR_|net::/.test(m.text())) errors.push(m.text()); });
  await page.route('https://cdnjs.cloudflare.com/**', (route) => threePath
    ? route.fulfill({ status: 200, contentType: 'application/javascript', body: fs.readFileSync(threePath) })
    : route.continue());
  await page.route('https://fonts.googleapis.com/**', (route) => (threePath ? route.fulfill({ status: 200, contentType: 'text/css', body: '' }) : route.continue()));
  await page.goto(pageUrl);
  await page.waitForFunction(() => window.__flavorCube && window.__flavorCube.three);
  await page.waitForTimeout(400);
  return { ctx, page, errors };
}
const overflow = (page) => page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);

for (const [label, viewport, scheme] of [['desktop-dark', { width: 1280, height: 900 }, 'dark'], ['phone-light', { width: 390, height: 844 }, 'light'], ['phone-dark', { width: 390, height: 844 }, 'dark'], ['desktop-light', { width: 1280, height: 900 }, 'light']]) {
  const { ctx, page, errors } = await open(viewport, scheme);
  check(label + ': 3D view built', await page.evaluate(() => !!window.__flavorCube.three));
  check(label + ': no horizontal overflow (mixing)', (await overflow(page)) <= 0, await overflow(page));
  // starting state
  const chi = await page.textContent('#chi');
  check(label + ': opens on NuFIT with chi2 0', chi.trim() === '0.00', chi);
  if (shots) await page.screenshot({ path: path.join(shots, label + '-mixing.png'), fullPage: false });
  // presets
  for (const name of ['TM1', 'Tri-bimaximal', 'No mixing']) {
    await page.click('.preset:has-text("' + name + '")');
    await page.waitForTimeout(250);
  }
  check(label + ': no-mixing chi2 2459', (await page.textContent('#chi')).trim() === '2459');
  await page.click('#secQ');
  await page.waitForTimeout(300);
  check(label + ': CKM opens at chi2 0', (await page.textContent('#chi')).trim() === '0.00', await page.textContent('#chi'));
  await page.click('.preset:has-text("sin")');
  await page.waitForTimeout(200);
  const sinChi = parseFloat(await page.textContent('#chi'));
  check(label + ': sin 3/13 chi2 = lambda pull squared', Math.abs(sinChi - Math.pow((3 / 13 - 0.22519) / 0.00083, 2)) < 0.1, sinChi);
  // slider moves the cube
  await page.click('#secL');
  await page.fill('#n12', '45');
  await page.dispatchEvent('#n12', 'change');
  const t12 = await page.evaluate(() => window.__flavorCube.state.ang.t12 * 180 / Math.PI);
  check(label + ': number input sets theta12', Math.abs(t12 - 45) < 1e-9, t12);
  await page.click('#playTurns');
  await page.waitForTimeout(4200);
  const rootOk = await page.evaluate(() => {
    const s = window.__flavorCube.state, P = window.__flavorCube.Pure, a = s.ang;
    const O = P.cubeRotation(a.t12, a.t13, a.t23, a.d).O, R = window.__flavorCube.three.getRoot();
    return O.every((r, i) => r.every((x, j) => Math.abs(x - R[i][j]) < 1e-9));
  });
  check(label + ': play-turns ends on the preset rotation', rootOk);
  // vertex
  await page.click('#tab-vertex');
  await page.waitForTimeout(900);
  check(label + ': no horizontal overflow (vertex)', (await overflow(page)) <= 0, await overflow(page));
  for (const p of ['J5', 'J6', 'J3']) { await page.click('[data-pair="' + p + '"]'); await page.waitForTimeout(120); }
  for (const i of ['szilassi', 'fano', 'torus']) { await page.click('[data-inset="' + i + '"]'); await page.waitForTimeout(80); }
  await page.check('#tFano');
  const nMoves = await page.locator('.mbtn').count();
  check(label + ': 24 Fano move buttons', nMoves === 24, nMoves);
  // apply every move once, then check the composite against the page's own group
  for (let i = 0; i < nMoves; i++) await page.locator('.mbtn').nth(i).click();
  await page.waitForTimeout(200);
  await page.evaluate(() => window.__flavorCube.three.finishAll());
  const fano = await page.evaluate(() => {
    const s = window.__flavorCube.state, R = window.__flavorCube.three.getRoot();
    return { same: s.fanoM.every((r, i) => r.every((x, j) => Math.abs(x - R[i][j]) < 1e-9)), det: window.__flavorCube.Pure.det(s.fanoM), n: s.fanoCount };
  });
  check(label + ': 24 Fano moves compose to an element of T_d shown on the cube', fano.same && Math.abs(Math.abs(fano.det) - 1) < 1e-12 && fano.n === 24, fano);
  await page.click('#vCorner');
  await page.waitForTimeout(800);
  if (shots) await page.screenshot({ path: path.join(shots, label + '-vertex.png'), fullPage: false });
  await page.click('#fanoReset');
  // puzzle
  await page.click('#tab-puzzle');
  await page.waitForTimeout(900);
  check(label + ': no horizontal overflow (puzzle)', (await overflow(page)) <= 0, await overflow(page));
  await page.click('#pScramble');
  await page.evaluate(() => window.__flavorCube.three.finishAll());
  const scr = await page.evaluate(() => ({ solved: window.__flavorCube.Pure.isSolved(window.__flavorCube.state.cube), n: window.__flavorCube.state.history.length, tw: window.__flavorCube.Pure.twistTotal(window.__flavorCube.state.cube) }));
  check(label + ': scramble makes 22 moves, twist total 0', scr.n === 22 && !scr.solved && scr.tw === 0, scr);
  if (shots) await page.screenshot({ path: path.join(shots, label + '-puzzle.png'), fullPage: false });
  await page.click('#pSolve');
  await page.evaluate(() => window.__flavorCube.three.finishAll());
  check(label + ': solve restores the cube', await page.evaluate(() => window.__flavorCube.Pure.isSolved(window.__flavorCube.state.cube)));
  await page.click('#pTwist');
  await page.evaluate(() => window.__flavorCube.three.finishAll());
  check(label + ': hand twist shows total 1', (await page.textContent('#twTotal')).trim() === '1');
  await page.keyboard.press('Escape');
  await page.focus('#cube');
  await page.keyboard.press('r');
  await page.evaluate(() => window.__flavorCube.three.finishAll());
  check(label + ': keyboard R turns a face', await page.evaluate(() => window.__flavorCube.state.history.slice(-1)[0] === 'R'));
  await page.click('#pReset');
  check(label + ': reset solves', await page.evaluate(() => window.__flavorCube.Pure.isSolved(window.__flavorCube.state.cube)) && (await page.textContent('#twTotal')).trim() === '0');
  if (shots) await page.screenshot({ path: path.join(shots, label + '-full.png'), fullPage: true });
  check(label + ': no console errors', errors.length === 0, errors);
  await ctx.close();
}
await browser.close();
console.log(fails ? `\n${fails} failed` : '\nall passed');
process.exit(fails ? 1 : 0);
