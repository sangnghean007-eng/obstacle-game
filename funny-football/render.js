// Xuất từng khung hình của scene.html ra JPEG bằng Playwright.
// Dùng: node render.js <thư_mục_ra> [fps] [danh_sách_giây_xem_thử]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2], fps = +(process.argv[3] || 30), only = process.argv[4];
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exit(1); });
  await page.goto('file://' + path.resolve(__dirname, 'scene.html') + '?render');
  await page.evaluate(() => document.fonts.load('900 40px Inter'));
  const times = only ? only.split(',').map(Number) : [...Array(Math.round(await page.evaluate(() => DURATION) * fps)).keys()].map(i => i / fps);
  for (let i = 0; i < times.length; i++) {
    const data = await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.92); }, times[i]);
    fs.writeFileSync(path.join(out, only ? `t${times[i]}.jpg` : `f${String(i).padStart(5, '0')}.jpg`), Buffer.from(data.split(',')[1], 'base64'));
  }
  await browser.close();
})();
