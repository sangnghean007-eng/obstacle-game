const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  p.on('pageerror', e => { console.error(e.message); process.exit(1); });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => document.fonts.load('900 40px Inter'));
  await (typeof page !== 'undefined' ? page : p).waitForFunction(() => window.NEY_IMG && NEY_IMG.complete && NEY_IMG.naturalWidth > 0);
  const d = await p.evaluate(() => { sheet(); return document.getElementById('c').toDataURL('image/jpeg', .9); });
  fs.writeFileSync(process.argv[2], Buffer.from(d.split(',')[1], 'base64')); await b.close(); })();
