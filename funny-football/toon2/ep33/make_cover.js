// cover = the revenge-slap frame of scene.html + two story lines (node ep33/make_cover.js out.png)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(17.83); ctx.setTransform(1, 0, 0, 1, 0, 0);
    const c = document.createElement('canvas'); c.width = W; c.height = H; c.getContext('2d').drawImage(cv, 0, 0);   // close-up: crop the two faces and fill the frame
    const z = 1.45, cx = 470, cy = 880, sw = W / z, sh = H / z; ctx.drawImage(c, cx - sw / 2, cy - sh / 2, sw, sh, 0, 0, W, H);
    card('26 slaps… 1 came back 😭', 540, 300, 74, { rot: -0.02 }); });
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
