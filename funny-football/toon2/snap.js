// snap.js <scene.html> <out.jpg> <t1,t2,...> [cols] — contact sheet of the given times (labels in yellow), for frame-sheet reviews
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [scene, out, ts, cols = 5] = process.argv.slice(2); const T = ts.split(',').map(Number);
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + path.resolve(scene) + '?render'); await p.evaluate(() => window.CAST_READY || null);
  const shots = []; for (const t of T) shots.push(await p.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.85); }, t));
  await p.setContent('<body style="margin:0;background:#222"><canvas id="s"></canvas></body>');
  await p.evaluate(async ({ shots, T, cols }) => { const w = 270, h = 480, rows = Math.ceil(shots.length / cols), s = document.getElementById('s'); s.width = w * cols; s.height = h * rows; const g = s.getContext('2d');
    for (let i = 0; i < shots.length; i++) { const im = new Image(); im.src = shots[i]; await im.decode(); g.drawImage(im, (i % cols) * w, Math.floor(i / cols) * h, w, h); g.fillStyle = '#ff0'; g.font = 'bold 26px sans-serif'; g.fillText(T[i].toFixed(2), (i % cols) * w + 6, Math.floor(i / cols) * h + 28); }
    window.SHEET = s.toDataURL('image/jpeg', 0.88); }, { shots, T, cols: +cols });
  require('fs').writeFileSync(out, Buffer.from((await p.evaluate(() => window.SHEET)).split(',')[1], 'base64')); if (errs.length) console.log('ERRORS:', errs.slice(0, 5).join(' | ')); await b.close(); })();
