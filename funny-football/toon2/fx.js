// fx.js — particles, living crowd, light (overhaul M2, 21 Nov 2026). Pure functions of time (deterministic for parallel renders).
//  FX.burst(ctx, kind, x, y, t, t0, o)   kinds: dust, sweat, tears, debris, confetti, smoke, water, sparks, grass
//  FX.crowd(ctx, t, o)                    300–800 tiny fans: idle bob, Mexican wave, jump on events, flags, phone lights
//  FX.spot(ctx, x, y, r, a) · FX.rim(...) · FX.flash(ctx, k) · FX.shadow(ctx, x, gy, lightX, h, s) · FX.godrays(ctx, x, y, t)
(function () {
  const R = (s) => { let h = (s * 2654435761) >>> 0; return () => { h ^= h << 13; h ^= h >>> 17; h ^= h << 5; return ((h >>> 0) % 100000) / 100000; }; };
  const K = {
    dust: { n: 26, sp: [120, 420], up: [-0.9, -0.1], g: 300, life: 1.1, size: [14, 40], col: ['rgba(210,190,150,A)', 'rgba(180,160,120,A)'], grow: 2.2, drag: 2.5 },
    sweat: { n: 14, sp: [300, 700], up: [-1, -0.3], g: 2400, life: 0.7, size: [6, 12], col: ['rgba(150,210,255,A)'], drop: true },
    tears: { n: 18, sp: [250, 500], up: [-0.6, 0.1], g: 2000, life: 0.9, size: [8, 14], col: ['rgba(120,200,255,A)'], drop: true },
    debris: { n: 22, sp: [500, 1300], up: [-1, -0.2], g: 2600, life: 1.4, size: [10, 26], col: ['#6b4423', '#999', '#ddd'], rect: true, bounce: true },
    confetti: { n: 70, sp: [300, 1100], up: [-1, -0.5], g: 700, life: 2.6, size: [10, 18], col: ['#ffd60a', '#ff3fb4', '#3fe0ff', '#5ad15a', '#fff', '#e63946'], rect: true, flutter: true, drag: 1.2 },
    smoke: { n: 16, sp: [40, 160], up: [-1, -0.6], g: -120, life: 2.0, size: [30, 70], col: ['rgba(60,60,66,A)', 'rgba(90,90,96,A)'], grow: 2.6, drag: 1.0 },
    water: { n: 40, sp: [300, 900], up: [-1, -0.2], g: 2200, life: 1.0, size: [5, 11], col: ['rgba(140,200,255,A)', 'rgba(220,240,255,A)'], drop: true },
    sparks: { n: 30, sp: [600, 1500], up: [-1, 1], g: 900, life: 0.5, size: [3, 6], col: ['#ffd60a', '#fff4b0', '#ff9a3c'], line: true },
    grass: { n: 24, sp: [250, 700], up: [-1, -0.4], g: 2200, life: 1.0, size: [8, 16], col: ['#3a9d4a', '#2e7d32', '#6fbf4a'], rect: true, bounce: true },
  };
  function burst(ctx, kind, x, y, t, t0, o = {}) {
    const k = Object.assign({}, K[kind], o), tau = t - t0; if (tau < 0 || tau > k.life) return; const r = R(Math.round(x * 7 + y * 13 + t0 * 1000) + kind.length), gy = o.ground ?? 1e9;
    for (let i = 0; i < (o.n || k.n); i++) {
      const a = Math.PI * (k.up[0] + (k.up[1] - k.up[0]) * r()) + (o.dir || 0), sp = k.sp[0] + (k.sp[1] - k.sp[0]) * r(), s0 = k.size[0] + (k.size[1] - k.size[0]) * r(), col = k.col[Math.floor(r() * k.col.length)];
      const life = k.life * (0.6 + 0.4 * r()); if (tau > life) continue; const q = tau / life, dr = k.drag ? Math.exp(-k.drag * tau) : 1;
      let px = x + Math.cos(a) * sp * (k.drag ? (1 - dr) / k.drag : tau), py = y + Math.sin(a) * sp * (k.drag ? (1 - dr) / k.drag : tau) + 0.5 * k.g * tau * tau;
      if (k.bounce && py > gy) py = gy - Math.abs(Math.sin(tau * 12)) * 20 * (1 - q);
      if (k.flutter) px += Math.sin(t * 9 + i) * 18 * q;
      const al = (1 - q) ** (k.grow ? 1.2 : 0.6), sz = s0 * (k.grow ? 1 + k.grow * q : 1); ctx.save(); ctx.globalAlpha *= Math.max(0, al); ctx.fillStyle = col.replace('A', '1'); ctx.strokeStyle = col.replace('A', '1');
      if (k.rect) { ctx.translate(px, py); ctx.rotate(t * 8 + i); ctx.fillRect(-sz / 2, -sz / 4, sz, sz / 2); }
      else if (k.line) { ctx.lineWidth = sz; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px - Math.cos(a) * sp * 0.03, py - Math.sin(a) * sp * 0.03); ctx.stroke(); }
      else if (k.drop) { ctx.translate(px, py); ctx.rotate(Math.atan2(Math.sin(a) * sp + k.g * tau, Math.cos(a) * sp) - Math.PI / 2); ctx.beginPath(); ctx.moveTo(0, -sz * 1.4); ctx.quadraticCurveTo(sz, 0, 0, sz); ctx.quadraticCurveTo(-sz, 0, 0, -sz * 1.4); ctx.fill(); }
      else { ctx.beginPath(); ctx.arc(px, py, sz, 0, 7); ctx.fill(); }
      ctx.restore();
    }
  }
  // living crowd in tiers: o = { y0, rows, cols:[team colours], wave: speed or 0, jump: 0..1, flags, phones, density }
  function crowd(ctx, t, o = {}) {
    const rows = o.rows || 8, y0 = o.y0 ?? 120, rowH = o.rowH || 62, W = o.w || 1300, x0 = o.x0 ?? -110, cols = o.cols || ['#c8102e', '#fff', '#046a38'], r = R(o.seed || 9);
    for (let row = 0; row < rows; row++) {
      const yy = y0 + row * rowH, sc = 0.55 + row * 0.07, n = Math.round((W / (34 * sc)) * (o.density || 1));
      ctx.fillStyle = `rgba(20,24,40,${0.9 - row * 0.05})`; ctx.fillRect(x0, yy + 30 * sc, W, rowH);
      for (let i = 0; i < n; i++) {
        const x = x0 + (i + r() * 0.6) * (W / n), c = cols[Math.floor(r() * cols.length)], skin = ['#f1c9a8', '#d9a27c', '#8a5a3c', '#e8b592'][Math.floor(r() * 4)], ph = r() * 6.28;
        const wave = o.wave ? Math.max(0, Math.sin((x / W) * 6.28 - t * o.wave)) ** 6 : 0, jump = (o.jump || 0) * Math.abs(Math.sin(t * 10 + ph)), bob = Math.sin(t * 3 + ph) * 2;
        const lift = (wave * 26 + jump * 18 + bob) * sc, armsUp = wave > 0.4 || (o.jump || 0) > 0.3;
        ctx.fillStyle = c; ctx.beginPath(); ctx.roundRect(x - 11 * sc, yy - lift, 22 * sc, 30 * sc, 6 * sc); ctx.fill();
        ctx.fillStyle = skin; ctx.beginPath(); ctx.arc(x, yy - lift - 8 * sc, 9 * sc, 0, 7); ctx.fill();
        if (armsUp) { ctx.strokeStyle = skin; ctx.lineWidth = 4 * sc; ctx.beginPath(); ctx.moveTo(x - 9 * sc, yy - lift); ctx.lineTo(x - 15 * sc, yy - lift - 22 * sc); ctx.moveTo(x + 9 * sc, yy - lift); ctx.lineTo(x + 15 * sc, yy - lift - 22 * sc); ctx.stroke(); }
        if (o.flags && r() < 0.05) { const fx = x + 12 * sc, fy = yy - lift - 40 * sc; ctx.strokeStyle = '#ddd'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(fx, fy + 30 * sc); ctx.lineTo(fx, fy); ctx.stroke(); ctx.fillStyle = cols[0]; ctx.beginPath(); ctx.moveTo(fx, fy); for (let k = 0; k <= 6; k++) ctx.lineTo(fx + k * 6 * sc, fy + Math.sin(t * 8 + k + ph) * 3 * sc); for (let k = 6; k >= 0; k--) ctx.lineTo(fx + k * 6 * sc, fy + 16 * sc + Math.sin(t * 8 + k + ph) * 3 * sc); ctx.fill(); }
        if (o.phones && r() < 0.08) { ctx.fillStyle = `rgba(255,255,230,${0.6 + 0.4 * Math.sin(t * 2 + ph)})`; ctx.beginPath(); ctx.arc(x + 8 * sc, yy - lift - 26 * sc, 3.2 * sc, 0, 7); ctx.fill(); }
      }
    }
  }
  function spot(ctx, x, y, r, a = 0.5, col = '255,245,210') { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, `rgba(${col},${a})`); g.addColorStop(1, `rgba(${col},0)`); ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2); ctx.restore(); }
  function darken(ctx, a, W = 1080, H = 1920) { ctx.save(); ctx.fillStyle = `rgba(0,0,10,${a})`; ctx.fillRect(-600, -600, W + 1200, H + 1200); ctx.restore(); }
  function godrays(ctx, x, y, t, o = {}) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; for (let i = 0; i < (o.n || 7); i++) { const a = (o.a0 ?? 1.2) + i * 0.12 + Math.sin(t * 0.5 + i) * 0.02, L = o.len || 2200; ctx.fillStyle = `rgba(${o.col || '255,240,200'},${(o.alpha || 0.06) * (1 + Math.sin(t + i))})`; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a) * L, y + Math.sin(a) * L); ctx.lineTo(x + Math.cos(a + 0.05) * L, y + Math.sin(a + 0.05) * L); ctx.fill(); } ctx.restore(); }
  function rim(ctx, drawFn, dx, dy, col = 'rgba(255,240,200,.9)') { ctx.save(); ctx.translate(dx, dy); ctx.globalCompositeOperation = 'source-atop'; drawFn(); ctx.restore(); }
  function flash(ctx, k, col = '255,255,255') { if (k <= 0 || k >= 1) return; ctx.save(); ctx.fillStyle = `rgba(${col},${(1 - k) * 0.85})`; ctx.fillRect(-600, -600, 2400, 3200); ctx.restore(); }
  function shadow(ctx, x, gy, lightX, h, s = 1) { const off = (x - lightX) * 0.25 * s, len = 160 * s + h * 0.1; ctx.save(); ctx.globalAlpha = Math.max(0.12, 0.38 - h / 2000); ctx.fillStyle = '#000'; ctx.beginPath(); ctx.ellipse(x + off, gy + 6, len * 0.7 + Math.abs(off) * 0.4, 22 * s, 0, 0, 7); ctx.fill(); ctx.restore(); }
  window.FX = { burst, crowd, spot, darken, godrays, rim, flash, shadow };
})();
