const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  p.on('pageerror', e => { console.error('ERR', e.message); process.exit(1); });
  await p.goto('file://' + path.resolve(process.argv[2])); await p.evaluate(pose => { window.POSE = pose; return go(); }, process.argv[4]);
  const d = await p.evaluate(() => document.getElementById('c').toDataURL('image/png'));
  require('fs').writeFileSync(process.argv[3], Buffer.from(d.split(',')[1], 'base64')); await b.close(); })();
