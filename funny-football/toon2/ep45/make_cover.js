// Ep45 cover: Barça debt collectors vs the giant 5/5 shield, Mbappé + Vinícius laughing above it
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(14.85); ctx.setTransform(1, 0, 0, 1, 0, 0); stamp('PAYBACK? 😤 …OUCH', 540, 300, 90, 1); card('Barça 4-1 · Real 5/5 🛡️', 540, 1740, 62, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
