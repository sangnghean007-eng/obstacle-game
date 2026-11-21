// styles.js — 5 style packs (overhaul M3, 21 Nov 2026). One pack per episode, never the previous episode's.
// Usage in a scene's render loop:  STYLE = STYLES.comic;  ...draw scene...;  STYLE.post(ctx, canvas, t);  then HUD text with STYLE.cap / STYLE.stamp / STYLE.bubble
//  comic  — halftone shadows, thick panel border, jagged SFX boxes, speed-line backdrop helper
//  ink    — paper texture, sepia ink wash, "boiling" hand-drawn wobble (changes every 3 frames), handwritten captions
//  retro  — 80s arcade: scanlines, RGB split, neon palette, pixel captions
//  noir   — black & white with ONE accent colour kept (default red), hard contrast, film grain, silent-film cards
//  poster — screen print: 2 flat inks + paper, 4-px misregistration, giant block type
(function () {
  const W = 1080, H = 1920;
  const base = (document.currentScript && document.currentScript.src || '').replace(/styles\.js.*$/, '') + 'fonts/';
  for (const [fam, file, w] of [['Bangers', 'bangers', '400'], ['Caveat', 'caveat', '700'], ['Press Start 2P', 'press-start-2p', '400'], ['Anton', 'anton', '400'], ['Playfair Display', 'playfair-display', '400']]) { try { const f = new FontFace(fam, `url(${base}${file}.woff2)`, { weight: w }); document.fonts.add(f); f.load(); } catch (e) {} } const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  let paper = null, dots = null, grain = [];
  function paperTex() { if (paper) return paper; paper = mk(540, 960); const g = paper.getContext('2d'); g.fillStyle = '#f3ead6'; g.fillRect(0, 0, 540, 960); const d = g.getImageData(0, 0, 540, 960); for (let i = 0; i < d.data.length; i += 4) { const n = (Math.random() - 0.5) * 26; d.data[i] += n; d.data[i + 1] += n; d.data[i + 2] += n * 0.8; } g.putImageData(d, 0, 0); g.globalAlpha = 0.08; g.strokeStyle = '#8a7a5a'; for (let i = 0; i < 260; i++) { g.lineWidth = Math.random() * 1.5; g.beginPath(); const x = Math.random() * 540, y = Math.random() * 960; g.moveTo(x, y); g.lineTo(x + (Math.random() - 0.5) * 60, y + (Math.random() - 0.5) * 6); g.stroke(); } return paper; }
  function dotTex() { if (dots) return dots; dots = mk(24, 24); const g = dots.getContext('2d'); g.fillStyle = '#000'; for (const [x, y] of [[6, 6], [18, 18]]) { g.beginPath(); g.arc(x, y, 5.2, 0, 7); g.fill(); } return dots; }
  function grainTex(k) { if (grain[k]) return grain[k]; const c = mk(270, 480), g = c.getContext('2d'), d = g.createImageData(270, 480); for (let i = 0; i < d.data.length; i += 4) { const v = Math.random() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 40; } g.putImageData(d, 0, 0); grain[k] = c; return c; }
  function snapshot(cv) { const c = mk(W, H); c.getContext('2d').drawImage(cv, 0, 0); return c; }
  function lum(ctx, fn) { const d = ctx.getImageData(0, 0, W, H), p = d.data; for (let i = 0; i < p.length; i += 4) fn(p, i, 0.299 * p[i] + 0.587 * p[i + 1] + 0.114 * p[i + 2]); ctx.putImageData(d, 0, 0); }
  function font(f, size, w = 900) { return `${w} ${size}px ${f}`; }
  function textBox(ctx, s, x, y, size, o) { ctx.save(); ctx.font = font(o.font, size, o.weight || 900); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; const tw = ctx.measureText(s).width;
    if (o.box) o.box(ctx, x, y, tw, size); if (o.stroke) { ctx.lineJoin = 'round'; ctx.lineWidth = size * (o.sw || 0.2); ctx.strokeStyle = o.stroke; ctx.strokeText(s, x, y); } ctx.fillStyle = o.fill; ctx.fillText(s, x, y); ctx.restore(); }
  const jag = (col, ink) => (ctx, x, y, tw, size) => { ctx.beginPath(); const rx = tw / 2 + size * 0.8, ry = size * 1.1; for (let i = 0; i < 28; i++) { const a = i / 28 * Math.PI * 2, r = i % 2 ? 0.78 : 1; ctx.lineTo(x + Math.cos(a) * rx * r, y + Math.sin(a) * ry * r); } ctx.closePath(); ctx.fillStyle = col; ctx.fill(); ctx.lineWidth = 8; ctx.strokeStyle = ink; ctx.stroke(); };
  const rect = (col, ink, lw = 6, pad = 0.6, rad = 0) => (ctx, x, y, tw, size) => { ctx.beginPath(); ctx.roundRect(x - tw / 2 - size * pad, y - size * 0.8, tw + size * pad * 2, size * 1.6, rad); ctx.fillStyle = col; ctx.fill(); if (ink) { ctx.lineWidth = lw; ctx.strokeStyle = ink; ctx.stroke(); } };
  const STYLES = {
    comic: { name: 'comic', font: '"Bangers","Impact",Inter,sans-serif', ink: '#111', outline: 10,
      bg(ctx, t, cols = ['#ffd60a', '#ff8a00']) { const g = ctx.createRadialGradient(W / 2, H * 0.45, 50, W / 2, H * 0.45, 1300); g.addColorStop(0, cols[0]); g.addColorStop(1, cols[1]); ctx.fillStyle = g; ctx.fillRect(-600, -600, W + 1200, H + 1200); ctx.save(); ctx.globalAlpha = 0.25; ctx.fillStyle = '#fff'; for (let i = 0; i < 48; i++) { const a = i / 48 * Math.PI * 2 + t * 0.05; ctx.beginPath(); ctx.moveTo(W / 2, H * 0.45); ctx.lineTo(W / 2 + Math.cos(a) * 2400, H * 0.45 + Math.sin(a) * 2400); ctx.lineTo(W / 2 + Math.cos(a + 0.04) * 2400, H * 0.45 + Math.sin(a + 0.04) * 2400); ctx.fill(); } ctx.restore(); },
      post(ctx, cv, t) { const s = snapshot(cv); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); // halftone in the shadows
        const pat = ctx.createPattern(dotTex(), 'repeat'); const m = mk(W, H), mg = m.getContext('2d'); mg.drawImage(s, 0, 0);
        lum(ctx, (p, i, l) => { for (let c = 0; c < 3; c++) p[i + c] = Math.max(0, Math.min(255, (p[i + c] - l) * 1.3 + l)); });
        lum(mg, (p, i, l) => { p[i] = p[i + 1] = p[i + 2] = 0; p[i + 3] = l < 60 ? 120 : l < 120 ? 70 : 0; }); mg.globalCompositeOperation = 'destination-in'; mg.fillStyle = pat; mg.fillRect(0, 0, W, H); ctx.drawImage(m, 0, 0);
        ctx.lineWidth = 26; ctx.strokeStyle = '#111'; ctx.strokeRect(13, 13, W - 26, H - 26); ctx.lineWidth = 8; ctx.strokeStyle = '#fff'; ctx.strokeRect(34, 34, W - 68, H - 68); ctx.restore(); },
      cap(ctx, s, x, y, size = 54) { textBox(ctx, s.toUpperCase(), x, y, size, { font: this.font, fill: '#111', box: rect('#fff8d0', '#111', 7, 0.5, 4) }); },
      stamp(ctx, s, x, y, size = 80) { ctx.save(); ctx.translate(x, y); ctx.rotate(-0.08); textBox(ctx, s.toUpperCase(), 0, 0, size, { font: this.font, fill: '#e63946', stroke: '#111', sw: 0.12, box: jag('#ffd60a', '#111') }); ctx.restore(); },
      bubble(ctx, s, x, y, size = 46) { textBox(ctx, s, x, y, size, { font: this.font, fill: '#111', box: (c, X, Y, tw, sz) => { c.beginPath(); c.ellipse(X, Y, tw / 2 + sz, sz * 1.25, 0, 0, 7); c.moveTo(X - 20, Y + sz * 1.1); c.lineTo(X - 60, Y + sz * 2.4); c.lineTo(X + 20, Y + sz * 1.15); c.fillStyle = '#fff'; c.fill(); c.lineWidth = 7; c.strokeStyle = '#111'; c.stroke(); } }); } },
    ink: { name: 'ink', font: '"Caveat","Comic Sans MS","Segoe Print",cursive', ink: '#2a1d12', outline: 6,
      bg(ctx) { ctx.drawImage(paperTex(), -100, -100, W + 200, H + 200); },
      post(ctx, cv, t) { const s = snapshot(cv); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H); ctx.drawImage(s, 0, 0);
        const k = Math.floor(t * 30 / 3); let r = (k * 9301 + 49297) % 233280; const rnd = () => (r = (r * 9301 + 49297) % 233280) / 233280; // boiling: strip displacement, new every 3 frames
        for (let y = 0; y < H; y += 48) { const dx = (rnd() - 0.5) * 4; ctx.drawImage(s, 0, y, W, 48, dx, y, W, 48); }
        lum(ctx, (p, i, l) => { const a = 0.42, q = l < 70 ? l * 0.55 : l; p[i] = p[i] * a + (q * 1.02 + 10) * (1 - a); p[i + 1] = p[i + 1] * a + (q * 0.93) * (1 - a); p[i + 2] = p[i + 2] * a + (q * 0.74) * (1 - a); });
        ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(paperTex(), 0, 0, W, H); ctx.restore(); },
      cap(ctx, s, x, y, size = 60) { textBox(ctx, s, x, y, size, { font: this.font, fill: '#2a1d12', weight: 700 }); ctx.save(); ctx.strokeStyle = '#2a1d12'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - 240, y + size * 0.7); ctx.quadraticCurveTo(x, y + size * 0.85, x + 240, y + size * 0.65); ctx.stroke(); ctx.restore(); },
      stamp(ctx, s, x, y, size = 84) { ctx.save(); ctx.translate(x, y); ctx.rotate(-0.06); textBox(ctx, s, 0, 0, size, { font: this.font, fill: '#a3261c', weight: 700 }); ctx.restore(); },
      bubble(ctx, s, x, y, size = 50) { textBox(ctx, s, x, y, size, { font: this.font, fill: '#2a1d12', weight: 700, box: (c, X, Y, tw, sz) => { c.beginPath(); c.ellipse(X, Y, tw / 2 + sz * 0.8, sz * 1.1, 0, 0, 7); c.lineWidth = 4; c.strokeStyle = '#2a1d12'; c.stroke(); } }); } },
    retro: { name: 'retro', font: '"Press Start 2P","Courier New",monospace', ink: '#120024', outline: 6,
      bg(ctx, t) { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#12002b'); g.addColorStop(0.55, '#5b0e7a'); g.addColorStop(1, '#ff2fa0'); ctx.fillStyle = g; ctx.fillRect(-600, -600, W + 1200, H + 1200);
        ctx.save(); ctx.strokeStyle = 'rgba(0,240,255,.55)'; ctx.lineWidth = 3; const hz = H * 0.62; for (let i = -20; i <= 20; i++) { ctx.beginPath(); ctx.moveTo(W / 2 + i * 40, hz); ctx.lineTo(W / 2 + i * 260, H + 200); ctx.stroke(); } for (let k = 0; k < 14; k++) { const y = hz + ((k + t * 1.5) % 14) ** 2 * 6; ctx.beginPath(); ctx.moveTo(-200, y); ctx.lineTo(W + 200, y); ctx.stroke(); }
        ctx.fillStyle = '#ffcc33'; ctx.beginPath(); ctx.arc(W / 2, hz - 120, 220, Math.PI, 0); ctx.fill(); ctx.restore(); },
      post(ctx, cv, t) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); const GM = [[18, 0, 43], [91, 14, 122], [255, 47, 160], [0, 240, 255], [255, 240, 200]];
        lum(ctx, (p, i, l) => { const x = l / 255 * 4, k = Math.min(3, Math.floor(x)), f = x - k, A = GM[k], B = GM[k + 1]; const m = 0.62; for (let c = 0; c < 3; c++) p[i + c] = p[i + c] * (1 - m) + (A[c] + (B[c] - A[c]) * f) * m; });
        const s = snapshot(cv); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.22; ctx.drawImage(s, 5, 0); ctx.drawImage(s, -5, 0); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
        ctx.fillStyle = 'rgba(0,0,0,.22)'; for (let y = 0; y < H; y += 6) ctx.fillRect(0, y, W, 2); const v = ctx.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.75); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.55)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H); ctx.restore(); },
      cap(ctx, s, x, y, size = 34) { textBox(ctx, s.toUpperCase(), x, y, size, { font: this.font, fill: '#00f0ff', weight: 400, box: rect('rgba(18,0,43,.85)', '#ff2fa0', 5, 0.6, 0) }); },
      stamp(ctx, s, x, y, size = 46) { textBox(ctx, s.toUpperCase(), x, y, size, { font: this.font, fill: '#ffcc33', stroke: '#ff2fa0', sw: 0.15, weight: 400 }); },
      bubble(ctx, s, x, y, size = 30) { textBox(ctx, s.toUpperCase(), x, y, size, { font: this.font, fill: '#fff', weight: 400, box: rect('#000', '#fff', 5, 0.7, 0) }); } },
    noir: { name: 'noir', font: '"Playfair Display","Georgia",serif', ink: '#000', outline: 7, accent: [200, 16, 46],
      bg(ctx) { ctx.fillStyle = '#222'; ctx.fillRect(-600, -600, W + 1200, H + 1200); },
      post(ctx, cv, t) { const [ar, ag, ab] = this.accent; ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
        lum(ctx, (p, i, l) => { const r = p[i], g = p[i + 1], b = p[i + 2]; const keep = r > 120 && r > g * 1.7 && r > b * 1.5; const c = Math.max(0, Math.min(255, (l - 128) * 1.45 + 128)); if (keep) { p[i] = Math.min(255, r * 1.05); p[i + 1] = g * 0.5; p[i + 2] = b * 0.5; } else { p[i] = p[i + 1] = p[i + 2] = c; } });
        ctx.globalAlpha = 0.9; ctx.drawImage(grainTex(Math.floor(t * 24) % 4), 0, 0, W, H); ctx.globalAlpha = 1; const v = ctx.createRadialGradient(W / 2, H / 2, H * 0.25, W / 2, H / 2, H * 0.7); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.7)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H); ctx.restore(); },
      cap(ctx, s, x, y, size = 50) { textBox(ctx, s, x, y, size, { font: this.font, fill: '#fff', weight: 700, box: (c, X, Y, tw, sz) => { c.fillStyle = '#000'; c.fillRect(X - tw / 2 - 50, Y - sz, tw + 100, sz * 2); c.strokeStyle = '#fff'; c.lineWidth = 3; c.strokeRect(X - tw / 2 - 40, Y - sz + 10, tw + 80, sz * 2 - 20); } }); },
      stamp(ctx, s, x, y, size = 76) { textBox(ctx, s, x, y, size, { font: this.font, fill: '#c8102e', stroke: '#000', sw: 0.08, weight: 900 }); },
      bubble(ctx, s, x, y, size = 44) { this.cap(ctx, s, x, y, size); } },
    poster: { name: 'poster', font: '"Anton","Impact","Arial Black",sans-serif', ink: '#1b1b1b', outline: 8, inks: ['#1d3557', '#e63946'], paper: [244, 237, 222],
      bg(ctx) { ctx.fillStyle = '#f4edde'; ctx.fillRect(-600, -600, W + 1200, H + 1200); },
      post(ctx, cv, t) { const s = snapshot(cv); const [c1, c2] = this.inks.map(h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]); const pp = this.paper; ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
        const a = mk(W, H), ag = a.getContext('2d'); ag.drawImage(s, 0, 0); lum(ag, (p, i, l) => { if (l < 95) { p[i] = c1[0]; p[i + 1] = c1[1]; p[i + 2] = c1[2]; } else { p[i + 3] = 0; } });
        const b = mk(W, H), bg = b.getContext('2d'); bg.drawImage(s, 0, 0); lum(bg, (p, i, l) => { const red = p[i] > p[i + 1] * 1.4 && p[i] > 110; if (l >= 95 && (l < 175 || red)) { p[i] = c2[0]; p[i + 1] = c2[1]; p[i + 2] = c2[2]; } else { p[i + 3] = 0; } });
        ctx.fillStyle = `rgb(${pp})`; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 0.95; ctx.drawImage(b, 4, 3); ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(a, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 0.25; ctx.drawImage(grainTex(1), 0, 0, W, H); ctx.restore(); },
      cap(ctx, s, x, y, size = 70) { textBox(ctx, s.toUpperCase(), x, y, size, { font: this.font, fill: '#1d3557', weight: 400 }); },
      stamp(ctx, s, x, y, size = 150) { textBox(ctx, s.toUpperCase(), x, y, size, { font: this.font, fill: '#e63946', weight: 400 }); },
      bubble(ctx, s, x, y, size = 48) { textBox(ctx, s.toUpperCase(), x, y, size, { font: this.font, fill: '#f4edde', weight: 400, box: rect('#1d3557', null, 0, 0.5, 0) }); } },
  };
  window.STYLES = STYLES;
})();
