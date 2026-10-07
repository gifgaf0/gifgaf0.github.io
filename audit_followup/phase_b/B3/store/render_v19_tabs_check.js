// Render the v1.9-family calculator offline, visit every tab by name, open the baryon neutron panel and the top-Zf
// sub-tabs, and report compile/runtime errors and the visible text per tab.
// Usage: node render_v19_tabs_check.js FILE.jsx LABEL [SCREENSHOT_PREFIX]
// Needs node_modules (react@18, react-dom@18, @babel/standalone@7, playwright-core) in the cwd and a static server
// on http://127.0.0.1:8765/ serving the cwd.
const fs = require('fs'), path = require('path');
const { chromium } = require(path.resolve('node_modules/playwright-core'));
const src = process.argv[2], label = process.argv[3] || 'v19', shot = process.argv[4];
const code = fs.readFileSync(src, 'utf8')
  .replace(/^import \{([^}]*)\} from "react";\s*$/m, 'const {$1} = React;')
  .replace(/^export default function (\w+)/m, 'window.__Main = function $1');
const base = 'http://127.0.0.1:8765/node_modules/';
const html = `<!doctype html><html><head><meta charset="utf-8"></head><body><div id="root"></div>
<script src="${base}react/umd/react.production.min.js"></script>
<script src="${base}react-dom/umd/react-dom.production.min.js"></script>
<script src="${base}@babel/standalone/babel.min.js"></script>
<script>
try {
  const out = Babel.transform(${JSON.stringify(code)}, { presets: ['react'] }).code;
  (0, eval)(out);
  ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(window.__Main));
} catch (e) { console.error('COMPILE/RUN: ' + e.message); }
</script></body></html>`;
const tmp = path.resolve(label + '_tabs_local.html');
fs.writeFileSync(tmp, html);
const TABS = ['MASS AUDIT', 'CALCULATOR', 'SPECTRUM', 'WORTICITY', 'GEN I', 'GEN II', 'GEN III', 'LEPTONS',
  'FORCE-RESIDUAL', 'NEUTRINOS', 'WEAK BOSONS', 'FINE STRUCTURE', 'BARYON ★', 'LENS EQ', 'COSMIC ECHOES',
  'FREEZE-OUT', 'TOP ZF ★'];
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1300, height: 1600 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text() + ' @ ' + (m.location().url || '')); });
  await page.goto('http://127.0.0.1:8765/' + path.basename(tmp));
  await page.waitForTimeout(2500);
  const out = { label, errors, header: '', tabs: {} };
  out.header = (await page.locator('#root').innerText()).slice(0, 900);
  for (const t of TABS) {
    const btn = page.getByRole('button', { name: t, exact: true });
    if (!(await btn.count())) { out.tabs[t] = 'TAB BUTTON NOT FOUND'; continue; }
    await btn.first().click(); await page.waitForTimeout(250);
    if (t === 'BARYON ★') {
      const nb = page.getByRole('button', { name: /NEUTRON/ });
      if (await nb.count()) { await nb.first().click(); await page.waitForTimeout(200); }
    }
    let txt = await page.locator('#root').innerText();
    if (t === 'TOP ZF ★') {
      for (const sub of ['FULL TABLE', 'EXPLORER', 'COMPARISON']) {
        const sb = page.getByRole('button', { name: sub, exact: true });
        if (await sb.count()) { await sb.first().click(); await page.waitForTimeout(200); txt += '\n[' + sub + ']\n' + await page.locator('#root').innerText(); }
      }
    }
    out.tabs[t] = txt.slice(900, 7000);
    if (shot && (t === 'WEAK BOSONS' || t === 'BARYON ★' || t === 'MASS AUDIT'))
      await page.screenshot({ path: `${shot}_${t.replace(/[^A-Z]/g, '')}.png`, fullPage: true });
  }
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
