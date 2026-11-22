// Ep39 cover: big Messi placing 937, Ronaldo's 986 above (big number)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render'); await p.evaluate(() => window.CAST_READY || null);
  await p.evaluate(() => { window.NO_HUD = true; render(0.5); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.save(); ctx.font = `400 150px ${FONT}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineWidth = 24; ctx.strokeStyle = INK; ctx.strokeText('937 vs 986', 540, 470); ctx.fillStyle = '#ffd23f'; ctx.fillText('937 vs 986', 540, 470); ctx.restore();
    card('Road to 1000 · Part 2 🧱', 540, 300, 60); card('GOALS 🧱 or TROPHIES 🏆?', 540, 1450, 58, { bg: '#fff3b0' }); });
  await p.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 }); await b.close(); })();
