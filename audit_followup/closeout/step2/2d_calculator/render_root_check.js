// Render the site root as it will be served: index.html (the stub) and archive/calculator_v3_1.html.
// React and Babel come from local node_modules in place of unpkg; everything else is the committed file.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright-core');
const repo = process.argv[2], shotDir = process.argv[3];
const site = path.join(__dirname, 'site_root');
fs.rmSync(site, { recursive: true, force: true });
fs.mkdirSync(path.join(site, 'archive'), { recursive: true });
const local = h => h.replace('https://unpkg.com/react@18/umd/react.production.min.js', '/node_modules/react/umd/react.production.min.js')
  .replace('https://unpkg.com/react-dom@18/umd/react-dom.production.min.js', '/node_modules/react-dom/umd/react-dom.production.min.js')
  .replace('https://unpkg.com/@babel/standalone/babel.min.js', '/node_modules/@babel/standalone/babel.min.js');
fs.writeFileSync(path.join(site, 'index.html'), local(fs.readFileSync(path.join(repo, 'index.html'), 'utf8')));
fs.writeFileSync(path.join(site, 'archive', 'calculator_v3_1.html'),
  local(fs.readFileSync(path.join(repo, 'archive', 'calculator_v3_1.html'), 'utf8')));
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const [label, w, h] of [['desktop', 1000, 1300], ['phone', 390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const errors = [], external = [];
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
    page.on('request', r => { if (!r.url().startsWith('http://127.0.0.1:8765/')) external.push(r.url()); });
    await page.goto('http://127.0.0.1:8765/site_root/index.html');
    const stub = { title: await page.title(), text: await page.locator('main').innerText(),
      href: await page.locator('main a').getAttribute('href'),
      hscroll: await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth) };
    if (shotDir) await page.screenshot({ path: path.join(shotDir, `stub_${label}.png`), fullPage: true });
    await page.locator('main a').click();
    await page.waitForLoadState('load');
    await page.waitForTimeout(2500);
    const arch = { url: page.url(), title: await page.title(),
      banner: await page.locator('.archive-banner').innerText(), tabs: {} };
    for (const t of ['Mass Audit', 'Calculator', 'Constants', 'Baryon', 'Spectrum', 'Worticity']) {
      const btn = page.locator('button', { hasText: new RegExp('^' + t + '$', 'i') }).first();
      if (await btn.count()) { await btn.click(); await page.waitForTimeout(250); }
      arch.tabs[t] = (await page.locator('#root').innerText()).length;
    }
    if (shotDir && label === 'desktop') await page.screenshot({ path: path.join(shotDir, 'archive_desktop.png') });
    out[label] = { stub, archive: arch, errors, external };
    await page.close();
  }
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
