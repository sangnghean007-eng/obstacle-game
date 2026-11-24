// Ep41 cover: Barça laughing with the trophy, Mbappé crying, scoreboard 36 · 33
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(20.2); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('9 WINS IN A ROW… STILL 2ND 😭', 540, 1640, 66, 1); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
