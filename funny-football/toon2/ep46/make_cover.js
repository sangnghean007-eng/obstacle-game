// Ep46 v3 cover: the "TOP 2*" banner over the Premier League table, Bruno at 19th
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(24.9); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp("19th = TOP 2?! 🙃", 540, 1520, 96, 1); card("Man Utd: 19th in BOTH leagues", 540, 1720, 50, { bg: "#fff3b0" }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
