// Ep36 cover (action text): the LIVERPOOL wrecking ball hits the MAN UTD house, Pochettino ducks
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(16.62); ctx.setTransform(1, 0, 0, 1, 0, 0); card('"Give me time" 🔨', 540, 300, 72, { bg: '#fff3b0' }); stamp('ANFIELD: 4-0 💥', 540, 460, 96, 1); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
