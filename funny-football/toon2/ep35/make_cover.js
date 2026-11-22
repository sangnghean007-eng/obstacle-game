// Ep35 cover: the tug-of-war over the disputed block, big number (cover type 'big-number', ≠ Ep34 action-text)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(19.9); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.save(); ctx.font = `400 210px ${FONT}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineWidth = 26; ctx.strokeStyle = INK; ctx.strokeText('986?!', 540, 560); ctx.fillStyle = '#ffd23f'; ctx.fillText('986?!', 540, 560); ctx.restore();
    card('Road to 1000 🧱', 540, 330, 64); card('MINE!!', 790, 1480, 80, { bg: '#fff3b0', rot: 0.04 }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
