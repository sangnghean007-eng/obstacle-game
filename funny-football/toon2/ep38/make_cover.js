// Ep38 cover (split): the two farewell posts side by side, World Cup bar through the ceiling, Ronaldo stunned
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(20.4); ctx.setTransform(1, 0, 0, 1, 0, 0); card('The LIKE race ❤️', 540, 300, 76); stamp('MESSI 70M+ 🏆', 540, 450, 92, 1, '#b8860b'); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
