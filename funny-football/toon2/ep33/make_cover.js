// cover = the revenge-slap frame of scene.html + two story lines (node ep33/make_cover.js out.png)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(17.83); ctx.setTransform(1, 0, 0, 1, 0, 0);
    card('9 wins = 26 slaps 🖐️', 540, 250, 76, { rot: -0.02 }); card('…then Celta slapped back 😭', 540, 370, 62, { rot: 0.02, bg: '#ffe9a8' }); });
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
