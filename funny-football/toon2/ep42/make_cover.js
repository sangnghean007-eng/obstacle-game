// Ep42 cover: Mbappé chasing, Dembélé waving two UCL trophies from the PSG motorbike
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(14.7); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('HOOKED 🎣😂', 540, 300, 100, 1); card('PSG 🏆🏆 · Mbappé 0', 540, 1740, 64, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
