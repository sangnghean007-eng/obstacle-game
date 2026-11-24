// Ep44 cover: Valverde's slap landing on laughing Raphinha, Yamal still laughing, TV "REAL 5-1 PSV"
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(4.65); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('KEEP LAUGHING 👋😏', 540, 300, 92, 1); card('Real 0-1 → 5-1 PSV', 540, 1740, 64, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
