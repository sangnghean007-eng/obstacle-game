// Ep37 cover (two-shot): Messi has just flipped the board to MESSI 8 · CR7 5, Ronaldo in shock
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(18.3); ctx.setTransform(1, 0, 0, 1, 0, 0);
    card('Ronaldo’s excuses 😤', 540, 330, 70); stamp('"the numbers don’t deceive"', 540, 470, 58, 1, '#7a4b00'); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
