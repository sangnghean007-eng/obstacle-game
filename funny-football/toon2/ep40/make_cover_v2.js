// Ep40 v2 cover (split): Mbappé | Yamal pointing at each other — "Worse miss?"
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(22.0); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('WORSE MISS? 👇', 540, 330, 96, 1); card('PEN ❌  vs  PEN ❌', 540, 1700, 60, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
