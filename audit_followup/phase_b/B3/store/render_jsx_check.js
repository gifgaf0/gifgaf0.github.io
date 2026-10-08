// Render a single-component .jsx file offline and report compile/runtime errors and the visible text.
// Usage: node render_jsx_check.js FILE.jsx LABEL [SCREENSHOT.png]
// Needs: node_modules with react@18, react-dom@18, @babel/standalone@7, playwright-core (resolved from the cwd),
//        and a static server on http://127.0.0.1:8765/ serving the cwd (python3 -m http.server 8765 --bind 127.0.0.1).
const fs = require('fs'), path = require('path');
const { chromium } = require(path.resolve('node_modules/playwright-core'));
const src = process.argv[2], label = process.argv[3] || 'jsx', shot = process.argv[4];
const code = fs.readFileSync(src, 'utf8')
  .replace(/^import \{([^}]*)\} from "react";\s*$/m, 'const {$1} = React;')
  .replace(/^export default function (\w+)/m, 'window.__Main = function $1');
const base = 'http://127.0.0.1:8765/node_modules/';
const html = `<!doctype html><html><head><meta charset="utf-8"></head><body style="background:#000"><div id="root"></div>
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
const tmp = path.resolve(label + '_jsx_local.html');
fs.writeFileSync(tmp, html);
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1000, height: 1400 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text() + ' @ ' + (m.location().url || '')); });
  await page.goto('http://127.0.0.1:8765/' + path.basename(tmp));
  await page.waitForTimeout(2500);
  const out = { label, errors, text: {} };
  out.text.initial = (await page.locator('#root').innerText()).slice(0, 6000);
  // click every button once (tabs, toggles) and collect text, to exercise each panel
  const n = await page.locator('button').count();
  for (let i = 0; i < n; i++) {
    const b = page.locator('button').nth(i);
    const t = (await b.innerText()).trim().slice(0, 40);
    try { await b.click({ timeout: 1000 }); await page.waitForTimeout(150); } catch (e) { continue; }
    out.text['after:' + t] = (await page.locator('#root').innerText()).slice(0, 6000);
  }
  // expand the first table row, if rows are clickable
  if (shot) await page.screenshot({ path: shot, fullPage: true });
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
