// Ep46 cover: the bar lying on the ground ("A DRAW") while Bruno carries the team over it
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(13.6); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp("MAN UTD'S BAR IN 2026 📉", 540, 300, 80, 1); card('1999: treble · 2026: "so proud" of a draw', 540, 1560, 46, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
