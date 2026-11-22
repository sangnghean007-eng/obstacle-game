// cover = the revenge-slap frame of scene.html + two story lines (node ep33/make_cover.js out.png)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(20.3); ctx.setTransform(1, 0, 0, 1, 0, 0);
    const c = document.createElement('canvas'); c.width = W; c.height = H; c.getContext('2d').drawImage(cv, 0, 0);
    const z = 1.55, cx = 540, cy = 1060, sw = W / z, sh = H / z; ctx.drawImage(c, cx - sw / 2, cy - sh / 2, sw, sh, 0, 0, W, H);   // the whole wrecked line, bigger
    card('9 wins = 26 slaps 🖐️', 540, 270, 76, { rot: -0.02 }); card('…in ONE line-up 😂 Who\'s next?', 540, 390, 58, { rot: 0.02, bg: '#ffe9a8' }); });
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
