// Ep40 v3 cover: the three on the sofa — Ronaldo & Mbappé laughing, Yamal crying in the middle; POST / WIDE / SKY
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(28.2); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('WHO LAUGHS LAST? 😂', 540, 330, 92, 1);
    [['POST', 250, 1010], ['WIDE', 540, 1420], ['SKY', 830, 1010]].forEach(l => stamp(l[0], l[1], l[2], 60, 1)); card('3 stars · 3 days · 3 missed pens', 540, 480, 50, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
