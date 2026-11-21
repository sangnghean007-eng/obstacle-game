// shots.js — camera grammar (overhaul M3, 21 Nov 2026). ≥5 shot types per episode, never the same type twice in a row.
// Each shot wraps a scene draw function:  SHOT.low(ctx, drawFn, { x, y, k })  — drawFn(ctx) draws the world in normal 1080x1920 coordinates.
//  wide   establishing, subject small                    cu     chest-up close shot
//  xcu    extreme close-up (face fills the frame)         low    worm's-eye: horizon low, subject towers, sky
//  high   bird's-eye: top-down pitch, tiny players        ots    over-the-shoulder: huge blurred foreground head/shoulder
//  dutch  tilted frame for tension                        split  2–3 panels, each its own shot
//  slowmo time remap + speed lines + afterimages (use SHOT.slow(t, t0, k))
(function () {
  const W = 1080, H = 1920;
  function cam(ctx, x, y, z, rot = 0, sx = 1, sy = 1) { ctx.translate(W / 2, H / 2); ctx.rotate(rot); ctx.scale(z * sx, z * sy); ctx.translate(-x, -y); }
  const SHOT = {
    wide(ctx, draw, o = {}) { ctx.save(); cam(ctx, o.x ?? 540, o.y ?? 960, o.zoom ?? 0.82); draw(ctx); ctx.restore(); },
    cu(ctx, draw, o = {}) { ctx.save(); cam(ctx, o.x ?? 540, o.y ?? 1250, o.zoom ?? 1.9); draw(ctx); ctx.restore(); },
    xcu(ctx, draw, o = {}) { ctx.save(); cam(ctx, o.x ?? 540, o.y ?? 1150, o.zoom ?? 3.2); draw(ctx); ctx.restore(); },
    low(ctx, draw, o = {}) { // camera on the grass looking up: anchor the feet near the bottom, stretch vertically
      ctx.save(); ctx.translate(0, (o.lift ?? 260)); cam(ctx, o.x ?? 540, o.y ?? 1250, o.zoom ?? 1.25, 0, 1, 1.18); draw(ctx); ctx.restore();
      const g = ctx.createLinearGradient(0, H * 0.82, 0, H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(20,60,20,.85)'); ctx.fillStyle = g; ctx.fillRect(0, H * 0.82, W, H * 0.18); },
    high(ctx, drawTop, o = {}) { ctx.save(); cam(ctx, o.x ?? 540, o.y ?? 960, o.zoom ?? 1, o.rot ?? 0); drawTop(ctx); ctx.restore(); },
    ots(ctx, draw, o = {}) { // foreground head + shoulder silhouette (blurred), subject sharp behind
      ctx.save(); cam(ctx, o.x ?? 540, o.y ?? 1250, o.zoom ?? 1.5); draw(ctx); ctx.restore();
      ctx.save(); ctx.filter = 'blur(10px)'; const side = o.side ?? -1, fx = side < 0 ? 120 : W - 120; ctx.fillStyle = o.fg || '#2a1a12';
      ctx.beginPath(); ctx.ellipse(fx, H * 0.62, 330, 380, 0, 0, 7); ctx.fill(); ctx.fillStyle = o.shirt || '#13294b'; ctx.beginPath(); ctx.ellipse(fx + side * -40, H * 1.02, 560, 380, 0, 0, 7); ctx.fill(); if (o.hair) { ctx.fillStyle = o.hair; ctx.beginPath(); ctx.ellipse(fx, H * 0.5, 320, 220, 0, Math.PI, 0); ctx.fill(); } ctx.restore(); },
    dutch(ctx, draw, o = {}) { ctx.save(); cam(ctx, o.x ?? 540, o.y ?? 1100, o.zoom ?? 1.25, o.rot ?? -0.24); draw(ctx); ctx.restore(); },
    split(ctx, panels, o = {}) { // panels: [{ draw, shot:'cu', opts }], vertical stack (default) or side by side
      const n = panels.length, vert = o.vertical ?? true, gap = 14;
      panels.forEach((p, i) => { ctx.save(); const x = vert ? 0 : i * W / n, y = vert ? i * H / n : 0, w = vert ? W : W / n, h = vert ? H / n : H; ctx.beginPath(); ctx.rect(x + gap / 2, y + gap / 2, w - gap, h - gap); ctx.clip();
        ctx.translate(x + w / 2 - W / 2, y + h / 2 - H / 2); SHOT[p.shot || 'cu'](ctx, p.draw, p.opts || {}); ctx.restore(); ctx.lineWidth = gap; ctx.strokeStyle = o.border || '#fff'; ctx.strokeRect(x + gap / 2, y + gap / 2, w - gap, h - gap); }); },
    slow(t, t0, k = 0.3) { return t < t0 ? t : t0 + (t - t0) * k; }, // remap time for slow motion from t0
    speedlines(ctx, t, o = {}) { ctx.save(); ctx.globalAlpha = o.alpha ?? 0.5; ctx.strokeStyle = o.col || '#fff'; for (let i = 0; i < (o.n || 26); i++) { const y = ((i * 197 + t * 2600) % (H + 400)) - 200, x = (i * 331) % W; ctx.lineWidth = 2 + (i % 4); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + (o.dx || 0), y + (o.len || 260)); ctx.stroke(); } ctx.restore(); },
  };
  SHOT.TYPES = ['wide', 'cu', 'xcu', 'low', 'high', 'ots', 'dutch', 'split', 'slowmo'];
  window.SHOT = SHOT;
})();
