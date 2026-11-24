// Ep43 cover: Ronaldo mid-leap to 988 with the VAR robot pulling the step away
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(10.5); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('988? VAR SAYS NO 🙅', 540, 300, 84, 1); card('987 / 1000 · 13 to go', 540, 1720, 62, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
