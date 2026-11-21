const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => { const [out, fps, a, b, scene] = process.argv.slice(2); const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(scene) + '?render'); await page.evaluate(() => document.fonts.load('900 40px Inter')); await page.evaluate(() => window.CAST_READY || null);
  for (let i = +a; i < +b; i++) { const d = await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.92); }, i / +fps); fs.writeFileSync(path.join(out, `f${String(i).padStart(5, '0')}.jpg`), Buffer.from(d.split(',')[1], 'base64')); }
  await browser.close(); })();
