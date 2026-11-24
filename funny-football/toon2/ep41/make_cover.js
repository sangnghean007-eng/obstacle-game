// Ep41 v2 cover: the slap — Yamal slapping Mbappé awake, cup behind his back, scoreboard 36 · 33
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(21.07); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('WAKE UP, KYLIAN 👋', 540, 1620, 80, 1); card('36 · 33 👀', 540, 1780, 60, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
