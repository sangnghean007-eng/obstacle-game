// chibi: big-head cartoon character system (head ~40% of height, no neck, seamless limbs,
// expressive eyes with lids/blink/look, many mouth shapes, 3/4 view facing left or right, squash & stretch).
// Original drawings. Real players are suggested only through public signifiers (kit colours, number, hair, beard).
(function () {
  const INK = '#22140c', OL = 7;
  let ctx;
  const D = a => a * Math.PI / 180;
  const go = (p, a, l) => [p[0] + Math.sin(D(a)) * l, p[1] + Math.cos(D(a)) * l];
  function path(pts) { ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); if (pts.length === 2) ctx.lineTo(pts[1][0], pts[1][1]); else { for (let i = 1; i < pts.length - 1; i++) { const mx = (pts[i][0] + pts[i + 1][0]) / 2, my = (pts[i][1] + pts[i + 1][1]) / 2; ctx.quadraticCurveTo(pts[i][0], pts[i][1], i === pts.length - 2 ? pts[i + 1][0] : mx, i === pts.length - 2 ? pts[i + 1][1] : my); } } }
  function stroke(pts, w, col) { path(pts); ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.lineWidth = w; ctx.strokeStyle = col; ctx.stroke(); }
  function blob(fn, fill, ol = OL) { ctx.beginPath(); fn(); if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (ol) { ctx.lineWidth = ol; ctx.strokeStyle = INK; ctx.lineJoin = 'round'; ctx.stroke(); } }
  function ell(x, y, rx, ry, fill, ol = OL, rot = 0) { blob(() => ctx.ellipse(x, y, Math.max(0.1, rx), Math.max(0.1, ry), rot, 0, Math.PI * 2), fill, ol); }
  function shade(clipFn, col, fn) { ctx.save(); ctx.beginPath(); clipFn(); ctx.clip(); ctx.fillStyle = col; ctx.beginPath(); fn(); ctx.fill(); ctx.restore(); }

  // ---------- limbs: one continuous capsule, outline drawn first so joints have no seams ----------
  function limbPts(root, a1, a2, l1, l2) { const k = go(root, a1, l1), e = go(k, a2, l2); return [root, k, e]; }
  function arm(C, root, ang, pass, side) {
    const [a1, a2] = ang, P = limbPts(root, a1, a2, C.arm * 0.5, C.arm * 0.5), w = C.armW, hr = w * 0.62;
    if (pass === 'ink') { stroke(P, w + 2 * OL, INK); ell(P[2][0], P[2][1], hr + OL / 2, hr + OL / 2, INK, 0); stroke(P.slice(0, 2).map((p, i) => i ? [P[0][0] + (P[1][0] - P[0][0]) * 0.55, P[0][1] + (P[1][1] - P[0][1]) * 0.55] : p), w * 1.25 + 2 * OL, INK); }
    else {
      stroke(P, w, C.skin);
      // muscle shading along the lower side of the limb
      ctx.save(); ctx.globalAlpha = 0.22; stroke(P.map(p => [p[0] + w * 0.18, p[1] + w * 0.12]), w * 0.45, '#000'); ctx.restore();
      const sl = [P[0], [P[0][0] + (P[1][0] - P[0][0]) * 0.55, P[0][1] + (P[1][1] - P[0][1]) * 0.55]]; stroke(sl, w * 1.25, C.kit.sleeve || C.kit.shirt); stroke([sl[1], sl[1]], w * 1.25, C.kit.cuff || C.kit.shirt);
      ell(P[2][0], P[2][1], hr, hr, C.kit.gloves || C.skin, 0); ell(P[2][0] - hr * 0.3, P[2][1] - hr * 0.35, hr * 0.35, hr * 0.25, 'rgba(255,255,255,.35)', 0);
      if (C.prop && C.prop.hand === side) C.prop.draw(P[2][0], P[2][1]);
    }
    return P[2];
  }
  function leg(C, root, ang, pass) {
    const [a1, a2] = ang, P = limbPts(root, a1, a2, C.leg * 0.5, C.leg * 0.5), w = C.legW, f = P[2];
    if (pass === 'ink') { stroke(P, w + 2 * OL, INK); blob(() => ctx.ellipse(f[0] + w * 0.35, f[1] + w * 0.05, w * 0.95 + OL / 2, w * 0.55 + OL / 2, 0, 0, Math.PI * 2), INK, 0); }
    else {
      stroke(P, w, C.skin);
      const s0 = [P[1][0] + (P[0][0] - P[1][0]) * 0.1, P[1][1] + (P[0][1] - P[1][1]) * 0.1]; stroke([s0, P[1], P[2]], w * 1.04, C.kit.sock);
      stroke([s0, [s0[0] + (P[2][0] - s0[0]) * 0.07, s0[1] + (P[2][1] - s0[1]) * 0.07]], w * 1.06, C.kit.sockBand || C.kit.sockShade || C.kit.sock);
      ell(f[0] + w * 0.35, f[1] + w * 0.05, w * 0.95, w * 0.55, C.kit.boot, 0); ell(f[0] + w * 0.6, f[1] - w * 0.15, w * 0.35, w * 0.14, 'rgba(255,255,255,.55)', 0);
    }
  }

  // ---------- heads ----------
  function eye(x, y, rx, ry, e, iris, side) {
    const lid = Math.min(1, e.lid || 0), lt = (e.lidTilt || 0) * side; // lidTilt > 0: angry (inner corner down)
    if (e.eyes === 'happy') { stroke([[x - rx, y + ry * 0.2], [x, y - ry * 0.55], [x + rx, y + ry * 0.2]], OL * 1.1, INK); return; }
    if (e.eyes === 'dizzy') { ctx.lineWidth = OL * 0.8; ctx.strokeStyle = INK; ctx.beginPath(); for (let i = 0; i < 40; i++) { const a = i * 0.45 + (window.T2T || 0) * 9, r = i / 40 * rx; ctx.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); } ctx.stroke(); return; }
    if (lid >= 0.95) { stroke([[x - rx, y], [x, y + ry * 0.25], [x + rx, y]], OL * 1.1, INK); return; }
    ell(x, y, rx, ry, '#fff', OL);
    ctx.save(); ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); ctx.clip();
    const lx = (e.look || [0, 0])[0] * rx * 0.35, ly = (e.look || [0, 0])[1] * ry * 0.3, ir = e.small ? rx * 0.38 : rx * 0.66;
    ell(x + lx, y + ly, ir, ir * 1.08, iris, 0); ell(x + lx, y + ly, ir * 0.55, ir * 0.6, INK, 0);
    ell(x + lx - ir * 0.35, y + ly - ir * 0.4, ir * 0.3, ir * 0.3, '#fff', 0); ell(x + lx + ir * 0.3, y + ly + ir * 0.35, ir * 0.13, ir * 0.13, '#fff', 0);
    if (lid > 0 || lt) { // eyelid covers the top part, tilted
      const yl = y - ry + 2 * ry * lid; ctx.fillStyle = e.lidCol; ctx.beginPath(); ctx.moveTo(x - rx - 2, y - ry - 4); ctx.lineTo(x + rx + 2, y - ry - 4); ctx.lineTo(x + rx + 2, yl + lt * ry * 0.8); ctx.lineTo(x - rx - 2, yl - lt * ry * 0.8); ctx.fill();
      ctx.restore(); stroke([[x - rx, yl - lt * ry * 0.8], [x + rx, yl + lt * ry * 0.8]], OL, INK);
    } else ctx.restore();
  }
  function mouth(x, y, w, m, C) {
    const h = w * 0.55, dark = '#5e1414', tongue = '#e0646a';
    const open = (pts, teeth, tng) => { blob(() => path(pts.concat([pts[0]])), dark); ctx.save(); ctx.beginPath(); path(pts.concat([pts[0]])); ctx.clip(); if (teeth) { ctx.fillStyle = '#fff'; ctx.fillRect(x - w, y - h, w * 2, h * 0.55); } if (tng) ell(x, y + h * 0.75, w * 0.5, h * 0.45, tongue, 0); ctx.restore(); blob(() => path(pts.concat([pts[0]])), null); };
    switch (m) {
      case 'smile': stroke([[x - w * 0.7, y - h * 0.1], [x, y + h * 0.45], [x + w * 0.7, y - h * 0.1]], OL * 1.1, INK); break;
      case 'smirk': stroke([[x - w * 0.6, y + h * 0.15], [x + w * 0.2, y + h * 0.2], [x + w * 0.7, y - h * 0.25]], OL * 1.1, INK); break;
      case 'flat': stroke([[x - w * 0.5, y + h * 0.1], [x + w * 0.5, y + h * 0.1]], OL * 1.1, INK); break;
      case 'bored': stroke([[x - w * 0.45, y + h * 0.2], [x + w * 0.45, y + h * 0.05]], OL * 1.1, INK); break;
      case 'grin': open([[x - w, y - h * 0.2], [x + w, y - h * 0.2], [x + w * 0.6, y + h * 0.7], [x - w * 0.6, y + h * 0.7]], true, true); break;
      case 'o': ell(x, y + h * 0.2, w * 0.32, h * 0.5, dark, OL); break;
      case 'yawn': ell(x, y + h * 0.4, w * 0.55, h * 1.05, dark, OL); ell(x, y + h * 0.95, w * 0.35, h * 0.35, tongue, 0); break;
      case 'shock': ell(x, y + h * 0.35, w * 0.45, h * 0.8, dark, OL); ell(x, y + h * 0.8, w * 0.3, h * 0.25, tongue, 0); break;
      case 'grit': { const pts = [[x - w * 0.85, y - h * 0.15], [x + w * 0.85, y - h * 0.15], [x + w * 0.75, y + h * 0.5], [x - w * 0.75, y + h * 0.5]]; blob(() => path(pts.concat([pts[0]])), '#fff'); for (let i = -2; i <= 2; i++) stroke([[x + i * w * 0.3, y - h * 0.15], [x + i * w * 0.3, y + h * 0.5]], 3, INK); stroke([[x - w * 0.8, y + h * 0.17], [x + w * 0.8, y + h * 0.17]], 3, INK); break; }
      case 'wavy': { const pts = []; for (let i = 0; i <= 8; i++) pts.push([x - w * 0.6 + i * w * 0.15, y + h * 0.2 + (i % 2 ? -1 : 1) * h * 0.12]); stroke(pts, OL * 0.9, INK); break; }
      case 'sip': ell(x, y + h * 0.15, w * 0.2, h * 0.22, dark, OL * 0.8); break;
      default: stroke([[x - w * 0.6, y], [x, y + h * 0.35], [x + w * 0.6, y]], OL * 1.1, INK);
    }
  }
  function hairBack(C, R) { const h = C.head; if (h.hair === 'curls') { const R2 = R * 1.12; for (let i = 0; i < 14; i++) { const a = Math.PI * (0.6 + i / 13 * 1.8); ell(Math.cos(a) * R2 * 1.02, -R * 0.15 + Math.sin(a) * R2 * 0.95 + (Math.sin(a) > 0.3 ? R * 0.2 : 0), R * 0.38, R * 0.36, h.hairCol, OL * 0.8); } } }
  function hairFront(C, R) {
    const h = C.head, hc = h.hairCol;
    if (h.hair === 'short') { blob(() => { ctx.moveTo(-R * 0.98, -R * 0.15); ctx.bezierCurveTo(-R * 1.05, -R * 1.05, R * 0.9, -R * 1.25, R * 1.0, -R * 0.2); ctx.quadraticCurveTo(R * 0.85, -R * 0.62, R * 0.3, -R * 0.66); ctx.quadraticCurveTo(-R * 0.4, -R * 0.7, -R * 0.75, -R * 0.35); ctx.closePath(); }, hc); ell(-R * 0.1, -R * 0.85, R * 0.35, R * 0.08, 'rgba(255,255,255,.28)', 0, -0.15); }
    if (h.hair === 'curls') { const pts = [[-1.0, -0.3], [-0.85, -0.7], [-0.5, -0.98], [-0.08, -1.1], [0.36, -1.04], [0.72, -0.85], [1.0, -0.5], [-0.3, -0.86], [0.15, -0.9], [0.55, -0.78]]; for (const [px, py] of pts) { ell(px * R, py * R, R * 0.3, R * 0.27, hc, OL * 0.8); stroke([[px * R - R * 0.14, py * R + R * 0.05], [px * R, py * R - R * 0.1], [px * R + R * 0.14, py * R + R * 0.04]], 3, 'rgba(255,255,255,.3)'); } }
    if (h.hair === 'quiff') { blob(() => { ctx.moveTo(-R * 0.98, -R * 0.1); ctx.bezierCurveTo(-R * 1.05, -R * 0.95, -R * 0.2, -R * 1.2, R * 0.2, -R * 1.12); ctx.bezierCurveTo(R * 0.55, -R * 1.5, R * 1.15, -R * 1.25, R * 1.0, -R * 0.75); ctx.quadraticCurveTo(R * 0.92, -R * 0.55, R * 1.0, -R * 0.3); ctx.quadraticCurveTo(R * 0.7, -R * 0.68, R * 0.15, -R * 0.7); ctx.quadraticCurveTo(-R * 0.45, -R * 0.68, -R * 0.78, -R * 0.3); ctx.closePath(); }, hc); ell(R * 0.45, -R * 1.12, R * 0.35, R * 0.09, 'rgba(255,255,255,.4)', 0, -0.4); stroke([[-R * 0.5, -R * 0.95], [R * 0.1, -R * 1.08], [R * 0.6, -R * 1.25]], 4, 'rgba(255,255,255,.25)'); }
    if (h.hair === 'bald') ell(-R * 0.15, -R * 0.75, R * 0.3, R * 0.1, 'rgba(255,255,255,.4)', 0, -0.3);
    if (h.hair === 'spiky') { blob(() => { ctx.moveTo(-R, -R * 0.2); for (let i = 0; i <= 8; i++) { const x = -R + i * R * 0.25; ctx.lineTo(x, -R * (i % 2 ? 1.35 : 0.7)); } ctx.lineTo(R, -R * 0.2); ctx.closePath(); }, hc); }
  }
  function head(C, e, t) {
    const R = C.head.R, h = C.head, sq = h.jaw || 0, fx = R * 0.22; // features shifted toward the facing side (3/4 view)
    hairBack(C, R);
    // ear on the near side
    ell(-R * 0.92, R * 0.08, R * 0.2, R * 0.26, C.skin, OL); ell(-R * 0.92, R * 0.08, R * 0.09, R * 0.14, C.shade, 0);
    const F = () => { ctx.moveTo(-R, 0); ctx.bezierCurveTo(-R, -R * 1.35, R * 1.05, -R * 1.35, R * 1.02, 0); ctx.bezierCurveTo(R * (1.0 + sq * 0.05), R * (0.7 + sq * 0.1), R * (0.45 + sq * 0.25), R * 1.0, 0, R * 1.0); ctx.bezierCurveTo(-R * (0.45 + sq * 0.25), R * 1.0, -R * (1.0 + sq * 0.05), R * (0.7 + sq * 0.1), -R, 0); ctx.closePath(); };
    blob(F, C.skin);
    shade(F, C.shade, () => { ctx.moveTo(R * 0.55, -R * 1.2); ctx.bezierCurveTo(R * 0.95, -R * 0.4, R * 0.9, R * 0.5, R * 0.3, R * 1.1); ctx.lineTo(R * 1.3, R * 1.2); ctx.lineTo(R * 1.3, -R * 1.3); ctx.closePath(); });
    shade(F, 'rgba(255,255,255,.18)', () => ctx.ellipse(-R * 0.35, -R * 0.45, R * 0.35, R * 0.25, -0.5, 0, Math.PI * 2));
    blob(F, null);
    if (h.beard) { const B = () => { ctx.moveTo(-R * 0.98, R * 0.05); ctx.bezierCurveTo(-R * 0.95, R * 0.8, -R * 0.3, R * 1.12, R * 0.15, R * 1.1); ctx.bezierCurveTo(R * 0.75, R * 1.05, R * 1.02, R * 0.6, R * 1.0, R * 0.05); ctx.quadraticCurveTo(R * 0.85, R * 0.45, R * 0.45, R * 0.5); ctx.quadraticCurveTo(fx, R * 0.32, R * 0.0, R * 0.5); ctx.quadraticCurveTo(-R * 0.5, R * 0.5, -R * 0.98, R * 0.05); ctx.closePath(); }; blob(B, h.beardCol || h.hairCol); }
    if (h.stubble) shade(F, 'rgba(60,40,30,.18)', () => { ctx.ellipse(fx * 0.5, R * 0.75, R * 0.85, R * 0.4, 0, 0, Math.PI * 2); });
    // cheeks
    ell(fx - R * 0.42, R * 0.32, R * 0.16, R * 0.09, 'rgba(240,110,100,.35)', 0); ell(fx + R * 0.55, R * 0.32, R * 0.12, R * 0.08, 'rgba(240,110,100,.3)', 0);
    // eyes
    const blink = e.blink ?? ((Math.floor((t + (C.blinkSeed || 0)) * 10) % 37) < 2), ex = R * 0.34, ey = -R * 0.08, rx = R * 0.2, ry = R * 0.26;
    const ee = Object.assign({ lidCol: C.skin }, e, blink && !e.noBlink ? { lid: 1 } : {});
    eye(fx - ex, ey, rx, ry, ee, h.iris || '#5a3a1e', -1); eye(fx + ex * 0.92, ey, rx * 0.88, ry, ee, h.iris || '#5a3a1e', 1);
    // brows
    const by = ey - ry - R * 0.12 - (e.brow || 0) * R * 0.15, bt = (e.browTilt || 0);
    for (const [bx, sd] of [[fx - ex, -1], [fx + ex * 0.92, 1]]) { ctx.save(); ctx.translate(bx, by); ctx.rotate(bt * sd * 0.45); blob(() => ctx.roundRect(-R * 0.22, -R * 0.07, R * 0.44, R * (h.browW || 0.13), R * 0.07), h.browCol || h.hairCol, OL * 0.6); ctx.restore(); }
    // nose
    blob(() => { ctx.moveTo(fx + R * 0.02, R * 0.08); ctx.quadraticCurveTo(fx + R * (0.28 + (h.nose || 0) * 0.1), R * 0.3, fx + R * 0.05, R * 0.34); }, null, OL * 0.8);
    ell(fx + R * 0.1, R * 0.3, R * 0.06 * (1 + (h.nose || 0)), R * 0.04, 'rgba(0,0,0,.18)', 0);
    if (h.beard) ell(fx + R * 0.02, R * 0.6, R * 0.38 * (h.mouthW || 1), R * 0.2, C.skin, 0);
    mouth(fx + R * 0.02, R * 0.56, R * 0.3 * (h.mouthW || 1), e.mouth || 'smile', C);
    hairFront(C, R);
    if (e.sweat) { const k = (t * 1.3) % 1; ctx.save(); ctx.globalAlpha = 1 - k * 0.5; blob(() => { const sx = R * 1.0, sy = -R * 0.55 + k * R * 0.5; ctx.moveTo(sx, sy - R * 0.2); ctx.quadraticCurveTo(sx + R * 0.14, sy, sx, sy + R * 0.1); ctx.quadraticCurveTo(sx - R * 0.14, sy, sx, sy - R * 0.2); }, '#9be3ff', OL * 0.6); ctx.restore(); }
    if (e.vein) { ctx.save(); ctx.translate(-R * 0.45, -R * 0.7); ctx.strokeStyle = '#e11d2a'; ctx.lineWidth = OL; ctx.lineCap = 'round'; for (const a of [0, 1.57, 3.14, 4.71]) { ctx.beginPath(); ctx.arc(Math.cos(a) * R * 0.1, Math.sin(a) * R * 0.1, R * 0.08, a + 0.8, a + 2.3); ctx.stroke(); } ctx.restore(); }
    if (e.red) shade(F, 'rgba(230,40,40,.25)', () => ctx.ellipse(0, 0, R * 1.2, R * 1.2, 0, 0, Math.PI * 2));
  }
  // ---------- body ----------
  function torsoPath(C) { const sw = C.shoulderW, ww = C.waistW, sy = C.shoulderY, hy = C.hipY; return () => { ctx.moveTo(-sw, sy + 40); ctx.quadraticCurveTo(-sw, sy - 6, -sw + 50, sy - 8); ctx.lineTo(sw - 50, sy - 8); ctx.quadraticCurveTo(sw, sy - 6, sw, sy + 40); ctx.quadraticCurveTo(sw * 0.9, (sy + hy) / 2, ww, hy + 6); ctx.lineTo(-ww, hy + 6); ctx.quadraticCurveTo(-sw * 0.9, (sy + hy) / 2, -sw, sy + 40); ctx.closePath(); }; }
  function torso(C) {
    const T = torsoPath(C), K = C.kit, sw = C.shoulderW, sy = C.shoulderY, hy = C.hipY;
    blob(T, K.shirt);
    if (K.stripes) shade(T, K.stripes, () => { for (let x = -sw; x < sw; x += 48) ctx.rect(x, sy - 20, 22, hy - sy + 40); });
    if (K.hstripe) shade(T, K.hstripe, () => { ctx.rect(-sw - 20, sy + (hy - sy) * 0.42, sw * 2 + 40, (hy - sy) * 0.22); });
    if (K.hstripe2) shade(T, K.hstripe2, () => { ctx.rect(-sw - 20, sy + (hy - sy) * 0.5, sw * 2 + 40, (hy - sy) * 0.07); });
    if (K.pattern === 'hawaii') shade(T, K.flower || '#ffd60a', () => { for (let i = 0; i < 14; i++) { const fx = -sw + ((i * 71) % (sw * 2)), fy = sy + ((i * 53) % (hy - sy)); for (let p = 0; p < 5; p++) { ctx.moveTo(fx + Math.cos(p * 1.256) * 12 + 9, fy + Math.sin(p * 1.256) * 12); ctx.arc(fx + Math.cos(p * 1.256) * 12, fy + Math.sin(p * 1.256) * 12, 9, 0, Math.PI * 2); } } });
    shade(T, 'rgba(0,0,0,.16)', () => { ctx.moveTo(sw * 0.35, sy - 20); ctx.quadraticCurveTo(sw * 0.15, (sy + hy) / 2, sw * 0.3, hy + 20); ctx.lineTo(sw + 20, hy + 20); ctx.lineTo(sw + 20, sy - 20); ctx.closePath(); });
    shade(T, 'rgba(255,255,255,.16)', () => ctx.ellipse(-sw * 0.45, sy + (hy - sy) * 0.25, sw * 0.3, (hy - sy) * 0.2, -0.3, 0, Math.PI * 2));
    if (C.pecs) { stroke([[-sw * 0.6, sy + (hy - sy) * 0.38], [-sw * 0.1, sy + (hy - sy) * 0.45], [sw * 0.05, sy + (hy - sy) * 0.3]], 4, 'rgba(0,0,0,.25)'); stroke([[sw * 0.15, sy + (hy - sy) * 0.42], [sw * 0.55, sy + (hy - sy) * 0.36]], 4, 'rgba(0,0,0,.2)'); }
    blob(() => { ctx.moveTo(-36, sy - 8); ctx.quadraticCurveTo(10, sy + 34, 56, sy - 8); }, null, OL);
    blob(() => { ctx.moveTo(-36, sy - 8); ctx.quadraticCurveTo(10, sy + 34, 56, sy - 8); ctx.lineTo(46, sy - 8); ctx.quadraticCurveTo(10, sy + 18, -26, sy - 8); ctx.closePath(); }, K.collar, OL * 0.6);
    if (C.num || C.name) { ctx.font = `900 ${C.numSize || 64}px Inter, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round'; ctx.lineWidth = 8; ctx.strokeStyle = INK; const nx = sw * 0.3, ny = sy + (hy - sy) * 0.45; ctx.save(); ctx.translate(nx, ny); ctx.scale(C.f < 0 ? -1 : 1, 1); ctx.fillStyle = K.num; if (C.num) { ctx.strokeText(C.num, 0, 0); ctx.fillText(C.num, 0, 0); } if (C.name) { ctx.font = `900 ${C.nameSize || 24}px Inter, sans-serif`; ctx.lineWidth = 5; ctx.strokeText(C.name, 0, (C.numSize || 64) * 0.62); ctx.fillText(C.name, 0, (C.numSize || 64) * 0.62); } ctx.restore(); }
    blob(T, null);
  }
  function shorts(C) { const K = C.kit, ww = C.waistW, hy = C.hipY, L = C.legW; blob(() => { ctx.moveTo(-ww - 4, hy - 6); ctx.lineTo(ww + 4, hy - 6); ctx.lineTo(ww + L * 0.45, hy + C.leg * 0.32); ctx.lineTo(L * 0.2, hy + C.leg * 0.32); ctx.lineTo(0, hy + C.leg * 0.12); ctx.lineTo(-L * 0.2, hy + C.leg * 0.32); ctx.lineTo(-ww - L * 0.45, hy + C.leg * 0.32); ctx.closePath(); }, K.shorts); }

  const POSES = {
    stand: { bArm: [-20, -10], fArm: [20, 10], bLeg: [-8, -4], fLeg: [8, 4] },
    shield: { bArm: [-70, -30], fArm: [70, 30], bLeg: [-16, -8], fLeg: [16, 8] },
    flex: { bArm: [-95, -175], fArm: [95, 175], bLeg: [-14, -6], fLeg: [14, 6] },
    push: { bArm: [80, 95], fArm: [70, 88], bLeg: [-35, -15], fLeg: [25, 40] },
    run1: { bArm: [50, 110], fArm: [-50, -20], bLeg: [-40, 10], fLeg: [40, -50] },
    run2: { bArm: [-50, -20], fArm: [50, 110], bLeg: [40, -50], fLeg: [-40, 10] },
    sip: { bArm: [-20, -10], fArm: [30, 160], bLeg: [-8, -4], fLeg: [8, 4] },
    phone: { bArm: [-20, -10], fArm: [40, 150], bLeg: [-8, -4], fLeg: [8, 4] },
    flick: { bArm: [-20, -10], fArm: [100, 150], bLeg: [-10, -4], fLeg: [10, 4] },
    flickOut: { bArm: [-20, -10], fArm: [120, 100], bLeg: [-10, -4], fLeg: [10, 4] },
    cling: { bArm: [150, 120], fArm: [140, 100], bLeg: [30, 70], fLeg: [50, 100] },
    flail: { bArm: [-150, -120], fArm: [160, 120], bLeg: [-50, -20], fLeg: [60, 20] },
    sit: { bArm: [-30, -10], fArm: [30, 10], bLeg: [80, 0], fLeg: [90, 0] },
    crawl: { bArm: [100, 80], fArm: [80, 70], bLeg: [100, -10], fLeg: [90, -20] },
    carry: { bArm: [-160, -100], fArm: [150, 110], bLeg: [-12, -6], fLeg: [12, 6] },
    wave: { bArm: [-20, -10], fArm: [150, 170], bLeg: [-8, -4], fLeg: [8, 4] },
  };
  function mix(a, b, k) { a = POSES[a] || a; b = POSES[b] || b; const o = {}; for (const key of ['bArm', 'fArm', 'bLeg', 'fLeg']) o[key] = [0, 1].map(i => a[key][i] + (b[key][i] - a[key][i]) * k); return o; }
  function layout(C) { C.hipY = -C.leg * 0.95; C.shoulderY = C.hipY - C.torsoH; C.headY = C.shoulderY - C.head.R * 0.72; return C; }
  // draw(ctx, char, pose, expr, x, y, s, opts) — opts: { f: 1 right / -1 left, sq: squash (+ = flatter), lean: radians, t }
  function draw(c2d, C0, pose, expr, x, y, s, o = {}) {
    ctx = c2d; const C = layout(Object.assign({}, C0)), P = typeof pose === 'string' ? POSES[pose] : pose, e = typeof expr === 'string' ? (EXPR[expr] || {}) : expr, t = o.t ?? (window.T2T || 0);
    C.prop = o.prop; C.f = o.f || 1;
    ctx.save(); ctx.translate(x, y); ctx.rotate(o.lean || 0); const sq = o.sq || 0; ctx.scale(s * (o.f || 1) * (1 + sq), s * (1 - sq));
    const br = Math.sin(t * 3.2 + (C.blinkSeed || 0)) * (o.still ? 0 : 1);
    const bs = [-C.shoulderW * 0.72, C.shoulderY + 30], fs = [C.shoulderW * 0.8, C.shoulderY + 30];
    const bh = [-C.waistW * 0.5, C.hipY], fh = [C.waistW * 0.5, C.hipY];
    // back limbs
    arm(C, bs, P.bArm, 'ink', 'b'); arm(C, bs, P.bArm, 'fill', 'b');
    leg(C, bh, P.bLeg, 'ink'); leg(C, fh, P.fLeg, 'ink'); leg(C, bh, P.bLeg, 'fill'); leg(C, fh, P.fLeg, 'fill');
    shorts(C);
    ctx.save(); ctx.translate(0, C.hipY); ctx.scale(1 + br * 0.006, 1 - br * 0.008); ctx.translate(0, -C.hipY); torso(C); ctx.restore();
    ctx.save(); ctx.translate(0, C.headY + br * 2); ctx.rotate((o.headTilt || 0)); head(C, e, t); ctx.restore();
    arm(C, fs, P.fArm, 'ink', 'f'); arm(C, fs, P.fArm, 'fill', 'f');
    ctx.restore();
  }
  const EXPR = {
    neutral: { mouth: 'smile' }, happy: { eyes: 'happy', mouth: 'grin' }, smile: { mouth: 'smile', brow: 0.2 },
    bored: { lid: 0.45, mouth: 'bored', look: [0.6, 0.2], brow: -0.2 }, smug: { lid: 0.35, mouth: 'smirk', browTilt: -0.3, brow: 0.1, look: [-0.5, 0.1] },
    shock: { mouth: 'shock', small: true, brow: 1, noBlink: true }, angry: { lidTilt: 0.35, browTilt: 0.6, mouth: 'grit', look: [0.6, 0], red: true },
    strain: { lidTilt: 0.5, lid: 0.25, browTilt: 0.7, mouth: 'grit', red: true, vein: true, sweat: true, noBlink: true }, dizzy: { eyes: 'dizzy', mouth: 'wavy' },
    yawn: { lid: 0.8, mouth: 'yawn', brow: 0.4, noBlink: true }, sip: { lid: 0.4, mouth: 'sip', look: [0.5, 0.3] }, phone: { lid: 0.3, mouth: 'flat', look: [0.6, 0.8] },
    sad: { browTilt: -0.6, mouth: 'wavy', look: [0, 0.5] }, grin: { mouth: 'grin', brow: 0.3 },
  };
  window.chibi = { draw, mix, POSES, EXPR, go };
})();
