// Render an index.html variant offline (React/Babel from local node_modules) and report errors and visible text per tab.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright-core');
const src = process.argv[2], label = process.argv[3] || 'page', shot = process.argv[4];
let html = fs.readFileSync(src, 'utf8');
const nm = path.resolve(__dirname, 'node_modules');
html = html.replace('https://unpkg.com/react@18/umd/react.production.min.js', 'http://127.0.0.1:8765/node_modules/react/umd/react.production.min.js')
           .replace('https://unpkg.com/react-dom@18/umd/react-dom.production.min.js', 'http://127.0.0.1:8765/node_modules/react-dom/umd/react-dom.production.min.js')
           .replace('https://unpkg.com/@babel/standalone/babel.min.js', 'http://127.0.0.1:8765/node_modules/@babel/standalone/babel.min.js');
const tmp = path.join(__dirname, label + '_local.html');
fs.writeFileSync(tmp, html);
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1000, height: 1400 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text() + ' @ ' + (m.location().url || '')); });
  await page.goto('http://127.0.0.1:8765/' + path.basename(tmp));
  await page.waitForTimeout(2500);
  const out = { label, errors, tabs: {} };
  const tabNames = ['Mass Audit', 'Calculator', 'Constants', 'Baryon', 'Spectrum', 'Worticity'];
  for (const t of tabNames) {
    const btn = page.locator('button', { hasText: new RegExp('^' + t + '$', 'i') }).first();
    if (await btn.count()) { await btn.click(); await page.waitForTimeout(300); }
    out.tabs[t] = (await page.locator('#root').innerText()).slice(0, 4000);
    if (shot && (t === 'Mass Audit' || t === 'Baryon')) await page.screenshot({ path: shot.replace('.png', '_' + t.replace(' ', '') + '.png'), fullPage: true });
  }
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
