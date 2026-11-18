// pro.js — "production layer" for toon2 episodes (option C upgrade, Nov 18 2026).
// Impact frames on every hit, whip-pan smears between shots, contact shadows, colour grade, vignette, film grain.
// Usage inside an episode's render(): PRO.frame(ctx, canvas, info) after the world is drawn and before the HUD.
(function () {
  const W = 1080, H = 1920; const grain = document.createElement('canvas'); grain.width = 512; grain.height = 512;
  { const g = grain.getContext('2d'), im = g.createImageData(512, 512); let s = 7; for (let i = 0; i < im.data.length; i += 4) { s = (s * 16807) % 2147483647; const v = (s % 255); im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; } g.putImageData(im, 0, 0); }
  const copy = document.createElement('canvas'); copy.width = W; copy.height = H; const cc = copy.getContext('2d');
  function impact(ctx, k, cx = W / 2, cy = H * 0.6) { // k: 0..1 over ~0.12 s
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    if (k < 0.5) { ctx.globalCompositeOperation = 'saturation'; ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, W, H); ctx.globalCompositeOperation = 'difference'; ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); cc.clearRect(0, 0, W, H); cc.drawImage(ctx.canvas, 0, 0); ctx.globalCompositeOperation = 'overlay'; ctx.drawImage(copy, 0, 0); ctx.drawImage(copy, 0, 0); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = 'rgba(255,236,236,1)'; ctx.fillRect(0, 0, W, H); ctx.globalCompositeOperation = 'source-over'; }
    ctx.strokeStyle = k < 0.5 ? 'rgba(0,0,0,.85)' : 'rgba(255,255,255,.7)'; let s = 11;
    for (let i = 0; i < 46; i++) { s = (s * 16807) % 2147483647; const a = (s % 6283) / 1000, r0 = 260 + (s % 300), r1 = 1600; ctx.lineWidth = 3 + (s % 9); ctx.beginPath(); ctx.moveTo(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0); ctx.lineTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1); ctx.stroke(); }
    ctx.restore(); }
  function whip(ctx, canvas, k, dir = 1) { // smear the finished frame sideways at the start of a shot
    if (k >= 1) return; const amt = (1 - k) * (1 - k) * 220 * dir; cc.clearRect(0, 0, W, H); cc.drawImage(canvas, 0, 0);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); for (let i = 1; i <= 6; i++) { ctx.globalAlpha = 0.16; ctx.drawImage(copy, amt * i / 6, 0); } ctx.restore(); }
  function grade(ctx, t, warm = 0) {
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    const v = ctx.createRadialGradient(W / 2, H * 0.48, H * 0.3, W / 2, H * 0.5, H * 0.78); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(10,6,20,.32)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'soft-light'; const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, warm ? 'rgba(255,170,90,.14)' : 'rgba(150,180,255,.10)'); g.addColorStop(1, warm ? 'rgba(255,110,70,.10)' : 'rgba(255,200,140,.10)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = 0.04; const ox = (Math.floor(t * 30) * 137) % 512, oy = (Math.floor(t * 30) * 271) % 512; for (let x = -ox; x < W; x += 512) for (let y = -oy; y < H; y += 512) ctx.drawImage(grain, x, y);
    ctx.restore(); }
  function shadow(ctx, x, groundY, flyH, s = 1) { const k = Math.max(0.25, 1 - flyH / 700); ctx.save(); ctx.globalAlpha = 0.32 * k; ctx.fillStyle = '#000'; ctx.beginPath(); ctx.ellipse(x, groundY + 6, 120 * s * k, 24 * s * k, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore(); }
  window.PRO = { impact, whip, grade, shadow };
})();
