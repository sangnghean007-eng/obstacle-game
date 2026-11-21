// cover = the BONK frame of scene.html + one line of story (node ep32/make_cover.js out.png)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(13.0); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('BONK', 790, 600, 130, 1);
    card('Ronaldo catches everyone…', 540, 250, 70, { rot: -0.02 }); card('…except the "next GOAT" 😭', 540, 365, 70, { rot: 0.02, bg: '#ffe9a8' }); });
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
