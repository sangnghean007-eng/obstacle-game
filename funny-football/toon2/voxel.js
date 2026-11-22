// voxel.js — isometric block world for the "block" format (Ep35, 22 Nov 2026). Original look: our own palette, ink outlines,
// 4x4 hand-shaded texture per face, labels painted on faces. Not a copy of any game (no game names, textures, mobs or UI).
//   VOX.S = cube edge (px) · VOX.p(x,y,z) → [sx,sy] world px · VOX.cube(ctx,x,y,z,col,{label, ghost, glow, tex, alpha})
//   VOX.reachArm(c, x, y, side, tx, ty) → {a, k}: arm angle + stretch so the hand lands on (tx,ty) (stretchL/stretchR on figure)
//   VOX.box(ctx,x,y,w,h,col,{d}) — front-facing block (characters/props), VOX.figure(ctx, o) — block person with a caricature head
(function () {
  const C30 = Math.cos(Math.PI / 6), VOX = { S: 56, ox: 0, oy: 0 };
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (h, k) => { const c = hex(h); return `rgb(${c.map(v => Math.max(0, Math.min(255, Math.round(k >= 1 ? v + (255 - v) * (k - 1) : v * k)))).join(',')})`; };
  const hash = (a, b, c) => { let h = (a * 374761393 + b * 668265263 + c * 2147483647) | 0; h = (h ^ (h >>> 13)) * 1274126177; return ((h ^ (h >>> 16)) >>> 0) / 4294967295; };
  VOX.mix = mix; VOX.hash = hash;
  VOX.p = (x, y, z) => [VOX.ox + (x - y) * VOX.S * C30, VOX.oy + (x + y) * VOX.S * 0.5 - z * VOX.S];
  function quad(ctx, a, b, c, d) { ctx.beginPath(); ctx.moveTo(...a); ctx.lineTo(...b); ctx.lineTo(...c); ctx.lineTo(...d); ctx.closePath(); }
  // texture: 4x4 cells on a face given by origin o and edge vectors u, v
  function tex(ctx, o, u, v, col, k0, seed) {
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const r = hash(seed, i, j); if (r < 0.45) continue;
      const a = [o[0] + u[0] * i / 4 + v[0] * j / 4, o[1] + u[1] * i / 4 + v[1] * j / 4];
      ctx.fillStyle = mix(col, k0 * (r > 0.8 ? 0.9 : 1.06)); quad(ctx, a, [a[0] + u[0] / 4, a[1] + u[1] / 4], [a[0] + u[0] / 4 + v[0] / 4, a[1] + u[1] / 4 + v[1] / 4], [a[0] + v[0] / 4, a[1] + v[1] / 4]); ctx.fill(); }
  }
  // cube occupying [x,x+1]×[y,y+1]×[z,z+1]; visible faces: top (+z), left (+y), right (+x)
  VOX.cube = function (ctx, x, y, z, col, o = {}) {
    const P = VOX.p, t = [P(x, y, z + 1), P(x + 1, y, z + 1), P(x + 1, y + 1, z + 1), P(x, y + 1, z + 1)];
    const l = [P(x, y + 1, z + 1), P(x + 1, y + 1, z + 1), P(x + 1, y + 1, z), P(x, y + 1, z)], r = [P(x + 1, y + 1, z + 1), P(x + 1, y, z + 1), P(x + 1, y, z), P(x + 1, y + 1, z)];
    ctx.save(); if (o.alpha != null) ctx.globalAlpha *= o.alpha;
    if (o.ghost) { ctx.setLineDash([8, 7]); ctx.lineWidth = 3; ctx.strokeStyle = o.ghost; ctx.fillStyle = 'rgba(255,255,255,.10)';
      for (const f of [t, l, r]) { quad(ctx, ...f); ctx.fill(); ctx.stroke(); } ctx.setLineDash([]); }
    else {
      if (o.glow) { ctx.shadowColor = o.glow; ctx.shadowBlur = 40; }
      const seed = (x * 31 + y * 17 + z * 7) | 0;
      ctx.fillStyle = mix(col, 1.18); quad(ctx, ...t); ctx.fill(); ctx.shadowBlur = 0;
      ctx.fillStyle = mix(col, 0.86); quad(ctx, ...l); ctx.fill(); ctx.fillStyle = mix(col, 0.66); quad(ctx, ...r); ctx.fill();
      if (o.tex !== false) { const V = (a, b) => [b[0] - a[0], b[1] - a[1]];
        tex(ctx, t[0], V(t[0], t[1]), V(t[0], t[3]), col, 1.18, seed); tex(ctx, l[0], V(l[0], l[1]), V(l[0], l[3]), col, 0.86, seed + 1); tex(ctx, r[0], V(r[0], r[1]), V(r[0], r[3]), col, 0.66, seed + 2); }
      ctx.lineJoin = 'round'; ctx.strokeStyle = o.ink || '#1a1410'; ctx.lineWidth = o.lw || 3.2; for (const f of [t, l, r]) { quad(ctx, ...f); ctx.stroke(); }
    }
    if (o.label) { // painted on the left (+y) face
      const a = l[0], u = [l[1][0] - a[0], l[1][1] - a[1]], v = [l[3][0] - a[0], l[3][1] - a[1]]; ctx.save(); ctx.transform(u[0] / 100, u[1] / 100, v[0] / 100, v[1] / 100, a[0], a[1]);
      ctx.font = `400 ${o.labelSize || 34}px ${o.font || '"Press Start 2P",monospace'}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.lineWidth = 7; ctx.strokeStyle = o.labelEdge || '#1a1410'; ctx.strokeText(o.label, 50, 54); ctx.fillStyle = o.labelCol || '#fffaf0'; ctx.fillText(o.label, 50, 54); ctx.restore(); }
    if (o.label2) { const a = r[0], u = [r[1][0] - a[0], r[1][1] - a[1]], v = [r[3][0] - a[0], r[3][1] - a[1]]; ctx.save(); ctx.transform(u[0] / 100, u[1] / 100, v[0] / 100, v[1] / 100, a[0], a[1]);
      ctx.font = `400 ${o.labelSize || 34}px ${o.font || '"Press Start 2P",monospace'}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineWidth = 7; ctx.strokeStyle = '#1a1410'; ctx.strokeText(o.label2, 50, 54); ctx.fillStyle = o.labelCol || '#fffaf0'; ctx.fillText(o.label2, 50, 54); ctx.restore(); }
    ctx.restore();
  };
  // front-facing block (for figures/props): front rect + right side + top, ink outline
  VOX.box = function (ctx, x, y, w, h, col, o = {}) {
    const d = o.d ?? Math.min(w, h) * 0.32, dx = d * C30, dy = -d * 0.5;
    ctx.fillStyle = mix(col, 0.66); quad(ctx, [x + w, y], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + w, y + h]); ctx.fill();
    ctx.fillStyle = mix(col, 1.2); quad(ctx, [x, y], [x + dx, y + dy], [x + w + dx, y + dy], [x + w, y]); ctx.fill();
    ctx.fillStyle = col; ctx.fillRect(x, y, w, h);
    if (o.tex !== false) { const seed = o.seed || 3; for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) { const r = hash(seed, i, j); if (r < 0.55) continue; ctx.fillStyle = mix(col, r > 0.85 ? 0.9 : 1.07); ctx.fillRect(x + w * i / 3, y + h * j / 3, w / 3, h / 3); } }
    ctx.lineJoin = 'round'; ctx.lineWidth = o.lw || 3; ctx.strokeStyle = '#1a1410'; ctx.strokeRect(x, y, w, h);
    quad(ctx, [x + w, y], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + w, y + h]); ctx.stroke(); quad(ctx, [x, y], [x + dx, y + dy], [x + w + dx, y + dy], [x + w, y]); ctx.stroke();
  };
  // block hand with finger notches (owner: hands always have fingers)
  function hand(ctx, w, col) { VOX.box(ctx, -w * 0.55, 0, w * 1.1, w * 0.95, col, { d: w * 0.25, tex: false, lw: 2.5 });
    ctx.strokeStyle = 'rgba(26,20,16,.75)'; ctx.lineWidth = 2; for (const f of [0.3, 0.5, 0.7]) { ctx.beginPath(); ctx.moveTo(-w * 0.55 + w * 1.1 * f, w * 0.55); ctx.lineTo(-w * 0.55 + w * 1.1 * f, w * 0.95); ctx.stroke(); }
    VOX.box(ctx, w * 0.42, w * 0.15, w * 0.3, w * 0.45, col, { d: w * 0.12, tex: false, lw: 2 }); }      // thumb
  // block person. o: x,y (feet), c (cube px), kit {shirt, trim, shorts, sock, boot, skin, num, numCol, name}, armL/armR/legL/legR (rad, 0 = down,
  // + = toward screen right), lean, bob, headFn(ctx, cx, cy, h) draws the head, hold(ctx, handsX, handsY) for an object held overhead/in front
  VOX.figure = function (ctx, o) {
    const c = o.c || VOX.S, k = o.kit, sk = k.skin || '#e0a878';
    const legH = 0.72 * c, legW = 0.3 * c, torW = 0.84 * c, torH = 0.8 * c, armW = 0.27 * c, armH = 0.74 * c;
    ctx.save(); ctx.translate(o.x, o.y + (o.bob || 0)); if (o.flip) ctx.scale(-1, 1); ctx.rotate(o.lean || 0); if (o.sq) ctx.scale(1 + o.sq, 1 - o.sq);
    if (o.shadow !== false) { ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(0, 2, c * 0.6, c * 0.16, 0, 0, 7); ctx.fill(); }
    const leg = (sx, a) => { ctx.save(); ctx.translate(sx, -legH); ctx.rotate(a || 0); VOX.box(ctx, -legW / 2, 0, legW, legH * 0.45, k.shorts, { d: legW * 0.3, seed: 5 });
      VOX.box(ctx, -legW / 2, legH * 0.45, legW, legH * 0.3, k.sock || sk, { d: legW * 0.3, tex: false }); VOX.box(ctx, -legW / 2, legH * 0.75, legW * 1.15, legH * 0.25, k.boot || '#111', { d: legW * 0.3, tex: false }); ctx.restore(); };
    const arm = (sx, a, front) => { ctx.save(); ctx.translate(sx, -legH - torH + armW * 0.3); ctx.rotate(a || 0); const st = front ? o.stretchL : o.stretchR; if (st) ctx.scale(1, st);   // cartoon rubber arm VOX.box(ctx, -armW / 2, 0, armW, armH * 0.4, k.shirt, { d: armW * 0.3, seed: 9 });
      VOX.box(ctx, -armW / 2, armH * 0.4, armW, armH * 0.45, sk, { d: armW * 0.3, tex: false }); ctx.translate(0, armH * 0.82); hand(ctx, armW, sk); ctx.restore(); };
    arm(torW / 2 + armW * 0.45, -(o.armR || 0), false);
    leg(-legW * 0.62, o.legL); leg(legW * 0.62, o.legR);
    VOX.box(ctx, -torW / 2, -legH - torH, torW, torH, k.shirt, { d: c * 0.3, seed: 11 });
    ctx.fillStyle = k.trim; ctx.fillRect(-torW / 2, -legH - torH, torW, c * 0.08); ctx.fillRect(-torW / 2, -legH - c * 0.08, torW, c * 0.08);
    if (k.num) { ctx.font = `400 ${c * 0.36}px "Press Start 2P",monospace`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = k.numCol || k.trim; ctx.fillText(k.num, 0, -legH - torH * 0.58); }
    if (k.name) { const fs = c * 0.11; ctx.font = `400 ${fs}px "Press Start 2P",monospace`; let w = ctx.measureText(k.name).width; const sc = Math.min(1, torW * 0.92 / w); ctx.save(); ctx.translate(0, -legH - torH * 0.22); ctx.scale(sc, 1);
      ctx.lineWidth = 4; ctx.strokeStyle = '#111'; ctx.strokeText(k.name, 0, 0); ctx.fillStyle = '#fff'; ctx.fillText(k.name, 0, 0); ctx.restore(); }
    arm(-torW / 2 - armW * 0.45, o.armL || 0, true);
    if (o.headFn) o.headFn(ctx, 0, -legH - torH - c * 0.05);
    if (o.hold) o.hold(ctx, 0, -legH - torH);
    ctx.restore();
    return { top: o.y - legH - torH - c * 1.1 };
  };
  VOX.reachArm = function (c, x, y, side, tx, ty) { const sx = x + side * (0.42 * c + 0.27 * c * 0.45), sy = y - 0.72 * c - 0.8 * c + 0.27 * c * 0.3, dx = tx - sx, dy = ty - sy, L = 0.74 * c;
    return { a: side < 0 ? Math.atan2(-dx, dy) : Math.atan2(dx, dy), k: Math.max(1, Math.hypot(dx, dy) / L) }; };
  window.VOX = VOX;
})();
