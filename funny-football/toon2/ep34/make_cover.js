const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(4.66); ctx.setTransform(1, 0, 0, 1, 0, 0); scoreBug(4.6);
    card('Messi’s throw-in had ONE target 🎯', 540, 400, 60, { rot: -0.02 }); stamp('BONK', 760, 600, 140, 1); });
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
