// toon2: editorial-caricature character system (long limbs, long neck, exaggerated faces,
// tapered brown ink, flat colour + one shade tone). Original drawings; real players are shown
// only through public signifiers (kit colours/numbers without logos, hair, beard, poses).
(function () {
  const INK = '#2a160c';
  let ctx;
  const P = (x, y) => [x, y];
  function spline(pts, closed = true) {
    const n = pts.length, Q = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < (closed ? n : n - 1); i++) { const p0 = Q(i - 1), p1 = Q(i), p2 = Q(i + 1), p3 = Q(i + 2);
      ctx.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
    if (closed) ctx.closePath();
  }
  function fill(pts, col) { ctx.beginPath(); spline(pts); ctx.fillStyle = col; ctx.fill(); }
  function ink(pts, w0, w1, col = INK, closed = false) {   // tapered stroke along a smooth curve
    const S = []; const n = pts.length, Q = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
    const segs = closed ? n : n - 1;
    for (let i = 0; i < segs; i++) { const p0 = Q(i - 1), p1 = Q(i), p2 = Q(i + 1), p3 = Q(i + 2);
      for (let k = 0; k < 12; k++) { const t = k / 12, t2 = t * t, t3 = t2 * t;
        S.push([0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]); } }
    S.push(closed ? S[0] : pts[n - 1]);
    ctx.strokeStyle = col; ctx.lineCap = 'round';
    for (let i = 0; i < S.length - 1; i++) { const u = i / (S.length - 1), w = closed ? (w0 + w1) / 2 + (w1 - w0) / 2 * Math.sin(u * 12) : w0 + (w1 - w0) * Math.sin(Math.PI * u);
      ctx.beginPath(); ctx.moveTo(S[i][0], S[i][1]); ctx.lineTo(S[i + 1][0], S[i + 1][1]); ctx.lineWidth = w; ctx.stroke(); }
  }
  function shape(pts, col, w0 = 3, w1 = 6) { fill(pts, col); ink(pts, w0, w1, INK, true); }
  function ell(x, y, rx, ry, col, lw = 0, rot = 0) { ctx.beginPath(); ctx.ellipse(x, y, rx, ry, rot, 0, Math.PI * 2); if (col) { ctx.fillStyle = col; ctx.fill(); } if (lw) { ctx.strokeStyle = INK; ctx.lineWidth = lw; ctx.stroke(); } }
  // tapered limb as a filled outline: a->b->c with widths
  function limb(pts, widths, col, shade) {
    const L = [], R = [];
    for (let i = 0; i < pts.length; i++) { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
      const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l, w = widths[i] / 2;
      L.push([pts[i][0] + nx * w, pts[i][1] + ny * w]); R.push([pts[i][0] - nx * w, pts[i][1] - ny * w]); }
    const outline = L.concat(R.reverse());
    fill(outline, col);
    if (shade) { ctx.save(); ctx.beginPath(); spline(outline); ctx.clip(); ctx.beginPath(); spline(R.slice().reverse().concat(pts.slice().reverse().map((p, i) => p)), false); ctx.lineWidth = 0; const half = R.slice().reverse().concat(pts.slice().reverse()); fill(half, shade); ctx.restore(); }
    if (shade) { const Li = L.map((p, i) => [p[0] + (pts[i][0] - p[0]) * 0.22, p[1] + (pts[i][1] - p[1]) * 0.22]); ink(Li, 2, 5, 'rgba(255,255,255,.32)'); }
    ink(L, 3, 6); ink(R.slice().reverse(), 3, 6);
    ink([L[0], R[R.length - 1]], 2, 3);
  }
  function hand(x, y, s, a, pose, skin) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s);
    if (pose === 'point') { shape([[-14, -6], [14, -8], [16, 22], [-14, 22]], skin, 2, 4); limb([[2, -6], [4, -44]], [12, 10], skin); }
    else if (pose === 'fist') shape([[-16, -14], [16, -14], [18, 14], [-16, 16]], skin, 2, 4);
    else { shape([[-16, -10], [14, -12], [16, 18], [-14, 20]], skin, 2, 4); for (const dx of [-12, -4, 4, 12]) limb([[dx, 16], [dx * 1.2, 40]], [9, 8], skin); }
    ctx.restore();
  }
  function boot(x, y, s, dir, col) { ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s); shape([[-20, -26], [16, -26], [34, -10], [70, 0], [72, 16], [-24, 16]], col, 3, 5); ell(36, -4, 18, 5, 'rgba(255,255,255,.55)', 0, 0.25); ink([[-4, -18], [22, -10]], 1, 3); ink([[2, -24], [26, -16]], 1, 3); fill([[-24, 8], [72, 8], [72, 16], [-24, 16]], 'rgba(0,0,0,.3)'); ctx.fillStyle = INK; for (let i = 0; i < 4; i++) ctx.fillRect(-14 + i * 22, 16, 8, 8); ctx.restore(); }

  // ---------------- body (shared rig) ----------------
  // pose: { lArm: [shoulder->elbow angle, elbow->hand angle], rArm, lLeg, rLeg, hands }, angles in degrees, 0 = down, + = towards +x
  const D = a => a * Math.PI / 180;
  const go = (p, a, l) => [p[0] + Math.sin(D(a)) * l, p[1] + Math.cos(D(a)) * l];
  function body(c, pose) {
    const K = c.kit;
    const sh = { l: [c.cx - c.shoulder, 600], r: [c.cx + c.shoulder, 600] }, hip = { l: [c.cx - 48, 900], r: [c.cx + 48, 900] };
    const legLen = c.leg, armLen = c.arm;
    const leg = (side) => {
      const [ta, sa] = pose[side + 'Leg'], h = hip[side], k = go(h, ta, legLen * 0.5), f = go(k, sa, legLen * 0.5);
      const km = [(h[0] + k[0]) / 2, (h[1] + k[1]) / 2]; limb([h, km, k], [70, 80, 54], c.skin, c.shade);
      const sockTop = [k[0] + (f[0] - k[0]) * 0.12, k[1] + (f[1] - k[1]) * 0.12];
      const cm = [sockTop[0] + (f[0] - sockTop[0]) * 0.35, sockTop[1] + (f[1] - sockTop[1]) * 0.35]; limb([sockTop, cm, f], [54, 62, 38], K.sock, K.sockShade); { const b0 = [sockTop[0] + (f[0] - sockTop[0]) * 0.08, sockTop[1] + (f[1] - sockTop[1]) * 0.08], b1 = [sockTop[0] + (f[0] - sockTop[0]) * 0.18, sockTop[1] + (f[1] - sockTop[1]) * 0.18]; limb([b0, b1], [58, 60], K.sockShade); }
      boot(f[0], f[1] + 8, 1.1, (pose.face || 1), K.boot);
    };
    leg('l'); leg('r');
    // shorts
    shape([[c.cx - c.waist - 6, 860], [c.cx + c.waist + 6, 860], [c.cx + c.waist + 18, 990], [c.cx + 8, 1000], [c.cx, 950], [c.cx - 8, 1000], [c.cx - c.waist - 18, 990]], K.shorts);
    fill([[c.cx + 14, 870], [c.cx + c.waist + 6, 870], [c.cx + c.waist + 16, 984], [c.cx + 10, 994]], 'rgba(0,0,0,.18)'); ink([[c.cx + c.waist + 2, 870], [c.cx + c.waist + 14, 984]], 2, 4, K.collar === K.shorts ? 'rgba(255,255,255,.6)' : K.collar); ink([[c.cx - 30, 900], [c.cx - 14, 960]], 1, 3, 'rgba(255,255,255,.18)');
    // torso (V shape) with one shade side
    const T = [[c.cx - c.shoulder - 10, 590], [c.cx - 40, 570], [c.cx + 40, 570], [c.cx + c.shoulder + 10, 590], [c.cx + c.shoulder - 6, 700], [c.cx + c.waist + 4, 880], [c.cx - c.waist - 4, 880], [c.cx - c.shoulder + 6, 700]];
    fill(T, K.shirt);
    if (K.stripes) { ctx.save(); ctx.beginPath(); spline(T); ctx.clip(); ctx.fillStyle = K.stripes; for (let x = c.cx - 200; x < c.cx + 200; x += 52) ctx.fillRect(x, 560, 26, 340); ctx.restore(); }
    ctx.save(); ctx.beginPath(); spline(T); ctx.clip(); fill([[c.cx + 30, 560], [c.cx + 300, 560], [c.cx + 300, 900], [c.cx + 20, 900]], 'rgba(0,0,0,.14)'); ctx.restore();
    ctx.save(); ctx.beginPath(); spline(T); ctx.clip(); const tg = ctx.createLinearGradient(0, 570, 0, 890); tg.addColorStop(0, 'rgba(255,255,255,.22)'); tg.addColorStop(.5, 'rgba(255,255,255,0)'); tg.addColorStop(1, 'rgba(0,0,0,.12)'); ctx.fillStyle = tg; ctx.fillRect(c.cx - 300, 560, 600, 340);
    fill([[c.cx - 300, 852], [c.cx + 300, 852], [c.cx + 300, 900], [c.cx - 300, 900]], 'rgba(0,0,0,.16)'); ctx.restore();
    ink([[c.cx - c.shoulder + 30, 640], [c.cx - 40, 690], [c.cx - 52, 760]], 1, 3.5, 'rgba(0,0,0,.2)'); ink([[c.cx + 60, 780], [c.cx + 20, 830], [c.cx + 34, 870]], 1, 3, 'rgba(0,0,0,.18)'); ink([[c.cx - 70, 820], [c.cx - 30, 860]], 1, 3, 'rgba(0,0,0,.16)');
    if (K.belly) { const b = K.belly; shape([[c.cx - c.waist - 20 * b, 760], [c.cx, 720], [c.cx + c.waist + 40 * b, 760], [c.cx + c.waist + 60 * b, 830], [c.cx + c.waist + 20 * b, 900], [c.cx, 910], [c.cx - c.waist - 10 * b, 880]], K.bellyCol || K.shirt, 2, 5); ell(c.cx + 30, 790, 30 * b, 16 * b, 'rgba(255,255,255,.18)'); }
    if (K.pattern === 'hawaii') { ctx.save(); ctx.beginPath(); spline(T); if (K.belly) { const b = K.belly; spline([[c.cx - c.waist - 20 * b, 760], [c.cx, 720], [c.cx + c.waist + 40 * b, 760], [c.cx + c.waist + 60 * b, 830], [c.cx + c.waist + 20 * b, 900], [c.cx, 910], [c.cx - c.waist - 10 * b, 880]]); } ctx.clip(); for (let i = 0; i < 20; i++) { const fx = c.cx - 150 + (i * 97) % (300 + (K.belly || 0) * 60), fy = 600 + (i * 53) % 300; for (let p = 0; p < 5; p++) ell(fx + Math.cos(p * 1.256) * 14, fy + Math.sin(p * 1.256) * 14, 10, 10, K.flower || '#ffd60a'); ell(fx, fy, 7, 7, '#ff4d6d'); fill([[fx + 20, fy + 10], [fx + 50, fy], [fx + 40, fy + 26]], '#2f9e44'); } ctx.restore(); }
    if (K.tie) { shape([[c.cx - 12, 600], [c.cx + 12, 600], [c.cx + 20, 760], [c.cx, 790], [c.cx - 20, 760]], K.tie, 2, 4); fill([[c.cx - 46, 570], [c.cx - 6, 600], [c.cx - 30, 700]], K.lapel || '#fff'); fill([[c.cx + 46, 570], [c.cx + 6, 600], [c.cx + 30, 700]], K.lapel || '#fff'); }
    ink(T, 3, 7, INK, true);
    if (c.abs) { ink([[c.cx - 6, 700], [c.cx - 4, 840]], 1, 3, 'rgba(0,0,0,.35)'); ink([[c.cx - 40, 740], [c.cx + 30, 742]], 1, 2.5, 'rgba(0,0,0,.25)'); ink([[c.cx - 36, 790], [c.cx + 28, 792]], 1, 2.5, 'rgba(0,0,0,.25)'); }
    shape([[c.cx - 46, 566], [c.cx, 610], [c.cx + 46, 566], [c.cx + 50, 580], [c.cx, 630], [c.cx - 50, 580]], K.collar, 2, 4);
    if (c.num) { ctx.font = '900 58px Inter, sans-serif'; ctx.textAlign = 'center'; ctx.fillStyle = K.num; ctx.lineWidth = 6; ctx.strokeStyle = INK; ctx.strokeText(c.num, c.cx + 6, 730); ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.fillText(c.num, c.cx + 10, 734); ctx.fillStyle = K.num; ctx.fillText(c.num, c.cx + 6, 730); }
    const arm = (side) => {
      const [ua, fa] = pose[side + 'Arm'], s0 = sh[side], e = go(s0, ua, armLen * 0.5), h = go(e, fa, armLen * 0.5);
      const bm = [(s0[0] + e[0]) / 2, (s0[1] + e[1]) / 2], fm = [e[0] + (h[0] - e[0]) * 0.35, e[1] + (h[1] - e[1]) * 0.35]; limb([s0, bm, e, fm, h], [58, 66, 44, 48, 32], c.skin, c.shade);
      limb([s0, go(s0, ua, armLen * 0.24)], [70, 62], K.shirt, null); limb([go(s0, ua, armLen * 0.2), go(s0, ua, armLen * 0.25)], [66, 62], K.collar, null); ell(s0[0], s0[1] + 6, 34, 30, K.shirt);
      if (K.stripes) { }
      hand(h[0], h[1], K.gloves ? 1.5 : 1.1, -D(fa) + Math.PI, (pose.hands || {})[side] || 'open', K.gloves || c.skin);
    };
    arm('l'); arm('r');
  }
  // ---------------- heads ----------------
  function tears(x, y, t) { for (const d of [-1, 1]) for (let i = 0; i < 7; i++) { const k = ((t * 2.5 + i / 7) % 1); ell(x + d * (40 + k * 200), y - k * 80 + k * k * 300, 9, 13, '#7fd3ff', 2); } }
  function wail(x, y, w, h) { const M = [[x - w, y], [x, y - h * 0.3], [x + w, y], [x + w * 0.6, y + h], [x, y + h * 1.1], [x - w * 0.6, y + h]]; fill(M, '#5a1010'); ctx.save(); ctx.beginPath(); spline(M); ctx.clip(); fill([[x - w, y - 40], [x + w, y - 40], [x + w, y + 8], [x - w, y + 8]], '#fff'); ell(x, y + h * 0.85, w * 0.5, h * 0.3, '#d9585c'); ctx.restore(); ink(M, 3, 6, INK, true); }

  function eye(ex, ey, rx, ry, iris, expr) {
    if (expr === 'happy' || expr === 'cry') { ink([[ex - rx, ey + 4], [ex, ey - 6], [ex + rx, ey + 4]], 3, 6); return; }
    if (expr === 'sleep') { ink([[ex - rx, ey - 2], [ex, ey + 6], [ex + rx, ey - 2]], 3, 6); ink([[ex - rx + 2, ey + 6], [ex - rx - 4, ey + 12]], 1, 2); return; }
    const sh = expr === 'shock', an = expr === 'angry';
    ell(ex, ey, rx, ry + (sh ? 6 : 0), '#fff', 3);
    ctx.save(); ctx.beginPath(); ctx.ellipse(ex, ey, rx, ry + (sh ? 6 : 0), 0, 0, Math.PI * 2); ctx.clip();
    const ir = sh ? rx * 0.38 : rx * 0.62; ell(ex + 3, ey + 1, ir, ir, iris); ell(ex + 3, ey + 1, ir * 0.5, ir * 0.5, INK); ell(ex + 3 - ir * 0.35, ey + 1 - ir * 0.4, ir * 0.28, ir * 0.28, '#fff');
    if (expr === 'smug' || an) fill([[ex - rx - 4, ey - ry - 8], [ex + rx + 4, ey - ry - 8], [ex + rx + 4, ey - (an ? 1 : 2)], [ex - rx - 4, ey - (an ? 4 : 2)]], an ? 'rgba(170,110,80,1)' : '#d9a07c');
    ctx.restore();
    ink([[ex - rx - 3, ey - 1], [ex - rx * 0.3, ey - ry - (sh ? 7 : 1)], [ex + rx + 3, ey - 3]], 3, 6);
  }
  function brow(x0, y0, x1, y1, col, tilt) { ctx.save(); ctx.translate((x0 + x1) / 2, (y0 + y1) / 2); ctx.rotate(tilt); const w = (x1 - x0) / 2; shape([[-w, 4], [-w * 0.2, -6], [w, -2], [w * 0.9, 6], [-w * 0.8, 10]], col, 1, 2); ctx.restore(); }
  function faceLight(F, cx, cy) { ctx.save(); ctx.beginPath(); spline(F); ctx.clip(); const g = ctx.createRadialGradient(cx, cy, 10, cx, cy, 200); g.addColorStop(0, 'rgba(255,240,220,.35)'); g.addColorStop(1, 'rgba(255,240,220,0)'); ctx.fillStyle = g; ctx.fillRect(cx - 250, cy - 250, 500, 500); ctx.restore(); }
  function headRonaldo(cx, expr) {
    const S = '#c98a5e', SH = '#a96d45';
    // long neck
    limb([[cx - 4, 470], [cx, 590]], [70, 80], S, SH);
    // ear
    shape([[cx - 92, 300], [cx - 118, 290], [cx - 124, 330], [cx - 104, 368], [cx - 86, 360]], S);
    // face: long, square strong jaw, big chin
    const F = [[cx - 90, 210], [cx - 20, 168], [cx + 70, 176], [cx + 104, 230], [cx + 110, 300], [cx + 104, 380], [cx + 84, 452], [cx + 40, 494], [cx - 20, 496], [cx - 70, 460], [cx - 92, 380], [cx - 98, 290]];
    fill(F, S);
    ctx.save(); ctx.beginPath(); spline(F); ctx.clip(); fill([[cx - 100, 200], [cx - 40, 220], [cx - 50, 400], [cx - 20, 500], [cx - 110, 500]], SH); ell(cx + 40, 380, 34, 20, 'rgba(230,110,90,.35)'); ctx.restore();
    faceLight(F, cx + 40, 270); ink([[cx - 6, 470], [cx + 40, 484], [cx + 80, 456]], 1, 3, 'rgba(0,0,0,.25)');
    ink(F, 3, 7, INK, true);
    ink([[cx - 106, 310], [cx - 100, 340]], 1, 3); 
    // slick quiff with shaved sides + shine
    shape([[cx - 96, 250], [cx - 104, 170], [cx - 70, 110], [cx - 10, 70], [cx + 70, 62], [cx + 120, 96], [cx + 110, 150], [cx + 60, 168], [cx - 10, 172], [cx - 70, 206]], '#1a120c', 3, 7);
    fill([[cx - 98, 252], [cx - 70, 210], [cx - 74, 300], [cx - 96, 330]], 'rgba(40,28,20,.55)');
    ink([[cx - 40, 120], [cx + 20, 86], [cx + 80, 84]], 2, 6, '#5a4434'); ink([[cx - 70, 150], [cx - 10, 110], [cx + 60, 106]], 2, 5, '#4a382a');
    ell(cx + 10, 92, 34, 9, 'rgba(255,255,255,.7)', 0, -0.25); ink([[cx - 80, 190], [cx - 30, 140], [cx + 40, 120]], 1, 3, '#6b5240'); ink([[cx - 90, 230], [cx - 60, 190]], 1, 2.5, '#6b5240'); for (let i = 0; i < 9; i++) ink([[cx - 94 + (i % 3) * 8, 262 + i * 8], [cx - 90 + (i % 3) * 8, 266 + i * 8]], 1, 2, 'rgba(0,0,0,.35)');
    // sharp groomed brows
    const bu = expr === 'shock' ? -14 : 0, bt = expr === 'angry' ? 0.32 : expr === 'sad' ? -0.25 : 0;
    brow(cx - 34, 252 + bu, cx + 30, 252 + bu, '#1a120c', bt); brow(cx + 50, 248 + bu, cx + 102, 248 + bu, '#1a120c', -bt);
    for (const ex of [cx - 4, cx + 76]) eye(ex, 282, 17, 10, '#5a3a1e', expr === 'cry' ? 'happy' : expr);
    // nose: long, straight, pointing right
    shape([[cx + 34, 290], [cx + 64, 350], [cx + 96, 372], [cx + 76, 388], [cx + 44, 382]], S, 2, 5);
    // mouth
    if (expr === 'cry') { wail(cx + 40, 418, 56, 60); tears(cx + 36, 286, window.T2T || 0); }
    else if (expr === 'shock') { ell(cx + 40, 436, 22, 34, '#5a1010', 4); }
    else if (expr === 'sad') { ink([[cx - 6, 438], [cx + 40, 424], [cx + 86, 440]], 3, 7); }
    else if (expr === 'angry') { const M = [[cx - 10, 420], [cx + 90, 418], [cx + 86, 452], [cx - 6, 454]]; fill(M, '#fffdf6'); ink([[cx - 8, 436], [cx + 88, 435]], 1, 3); for (let i = 1; i < 6; i++) ink([[cx - 8 + i * 16, 420], [cx - 8 + i * 16, 452]], 1, 2, 'rgba(0,0,0,.3)'); ink(M, 3, 6, INK, true); }
    else if (expr === 'sleep') { ell(cx + 40, 436, 14, 10, '#5a1010', 3); }
    else { // signature huge grin
      const M = [[cx - 26, 412], [cx + 40, 406], [cx + 104, 408], [cx + 92, 452], [cx + 40, 472], [cx - 14, 452]];
      fill(M, '#5a1010'); ctx.save(); ctx.beginPath(); spline(M); ctx.clip(); fill([[cx - 40, 396], [cx + 120, 396], [cx + 120, 438], [cx - 40, 438]], '#fffdf6');
      for (let i = 0; i < 6; i++) ink([[cx - 10 + i * 20, 404], [cx - 10 + i * 20, 436]], 1, 2, 'rgba(0,0,0,.25)'); ctx.restore(); ink(M, 3, 6, INK, true);
    }
  }
  function headMessi(cx, expr) {
    const S = '#e6b38d', SH = '#c8916b';
    limb([[cx - 4, 470], [cx, 590]], [62, 70], S, SH);
    shape([[cx - 88, 310], [cx - 112, 300], [cx - 116, 340], [cx - 98, 374], [cx - 82, 366]], S);
    // rounder, softer face
    const F = [[cx - 88, 230], [cx - 30, 180], [cx + 60, 184], [cx + 100, 236], [cx + 108, 310], [cx + 96, 390], [cx + 60, 450], [cx, 470], [cx - 56, 446], [cx - 88, 380], [cx - 96, 300]];
    fill(F, S);
    ctx.save(); ctx.beginPath(); spline(F); ctx.clip(); fill([[cx - 100, 220], [cx - 50, 240], [cx - 56, 400], [cx - 110, 420]], SH); ell(cx + 40, 352, 30, 18, 'rgba(230,110,90,.35)'); ctx.restore();
    faceLight(F, cx + 30, 280);
    ink(F, 3, 7, INK, true);
    // full trimmed beard + moustache
    shape([[cx - 92, 330], [cx - 80, 400], [cx - 40, 462], [cx + 10, 486], [cx + 64, 460], [cx + 100, 396], [cx + 106, 330], [cx + 86, 380], [cx + 50, 400], [cx + 20, 384], [cx - 10, 392], [cx - 50, 380], [cx - 80, 350]], '#5b3a24', 2, 5);
    { const Rr = (i) => Math.sin(i * 12.9898) * 0.5 + 0.5; for (let i = 0; i < 26; i++) { const a = Rr(i), b = Rr(i + 40); const x = cx - 70 + a * 160, y = 400 + b * 70 - Math.abs(x - cx - 10) * 0.25; ink([[x, y], [x - 3 + (x - cx) * 0.04, y + 14]], 1, 2.5, '#3a2416'); } }
    ink([[cx - 6, 396], [cx + 30, 386], [cx + 80, 394]], 2, 5, '#3a2416');
    // side-swept fringe
    shape([[cx - 98, 300], [cx - 104, 220], [cx - 60, 166], [cx + 20, 150], [cx + 90, 170], [cx + 112, 230], [cx + 70, 214], [cx + 20, 226], [cx - 30, 220], [cx - 66, 250]], '#3b2416', 3, 7);
    ink([[cx - 40, 190], [cx + 20, 200], [cx + 80, 196]], 1, 4, '#6b4a30'); ink([[cx - 70, 200], [cx - 20, 180], [cx + 50, 176]], 1, 3.5, '#7a5638'); ink([[cx - 90, 260], [cx - 70, 210], [cx - 30, 190]], 1, 3, '#6b4a30'); ell(cx + 10, 172, 36, 8, 'rgba(255,255,255,.35)', 0, -0.12);
    // soft brows, calm eyes
    const bu = expr === 'shock' ? -12 : expr === 'sleep' ? 4 : 0, bt = expr === 'angry' ? 0.3 : expr === 'sad' ? -0.25 : expr === 'smug' ? -0.12 : 0;
    brow(cx - 34, 262 + bu, cx + 24, 262 + bu, '#3b2416', bt); brow(cx + 46, 260 + bu, cx + 96, 260 + bu, '#3b2416', -bt);
    for (const ex of [cx - 6, cx + 70]) eye(ex, 292, 15, 10, '#6b4423', expr);
    // rounded nose
    shape([[cx + 30, 300], [cx + 52, 344], [cx + 76, 356], [cx + 60, 372], [cx + 34, 364]], S, 2, 5);
    // mouth inside beard
    if (expr === 'cry') { wail(cx + 34, 410, 40, 46); tears(cx + 32, 294, window.T2T || 0); }
    else if (expr === 'shock') ell(cx + 34, 418, 16, 24, '#5a1010', 4);
    else if (expr === 'sad') ink([[cx + 4, 418], [cx + 34, 410], [cx + 64, 420]], 3, 6);
    else if (expr === 'sleep') { ell(cx + 34, 416, 12, 9, '#5a1010', 3); ell(cx + 50, 428, 5, 9, '#bfe7ff', 2); }
    else if (expr === 'smug') ink([[cx + 6, 414], [cx + 36, 416], [cx + 66, 402]], 3, 6);
    else { const M = [[cx + 2, 404], [cx + 34, 400], [cx + 68, 404], [cx + 56, 426], [cx + 34, 434], [cx + 12, 426]]; fill(M, '#6a1a14'); ctx.save(); ctx.beginPath(); spline(M); ctx.clip(); fill([[cx - 10, 396], [cx + 80, 396], [cx + 80, 412], [cx - 10, 412]], '#fff'); ctx.restore(); ink(M, 2, 5, INK, true); }
  }
  // ---------------- generic heads for the supporting cast ----------------
  function headGeneric(cx, expr, h, c) {
    const S = c.skin, SH = c.shade, HC = h.hairCol || '#2a1a10';
    limb([[cx - 4, 470], [cx, 590]], [h.neck || 62, (h.neck || 62) + 8], S, SH);
    if (h.hair === 'long' || h.hair === 'bun') shape([[cx - 110, 250], [cx - 130, 420], [cx - 90, 520], [cx + 40, 500], [cx + 100, 400], [cx + 110, 260]], HC, 3, 6);
    if (h.hair === 'afro') { for (let i = 0; i < 14; i++) { const a = Math.PI * (0.95 + i / 13 * 1.1); ell(cx + 6 + Math.cos(a) * 120, 260 + Math.sin(a) * 120, 52, 52, HC, 3); } ell(cx + 6, 240, 120, 110, HC); }
    shape([[cx - 86, 310], [cx - 110, 300], [cx - 114, 340], [cx - 96, 372], [cx - 80, 366]], S);
    const f = h.face || 'round', w = h.wide || 1;
    const F = f === 'long' ? [[cx - 80, 220], [cx - 20, 170], [cx + 60, 176], [cx + 94, 230], [cx + 100, 330], [cx + 86, 430], [cx + 40, 492], [cx - 20, 494], [cx - 66, 440], [cx - 86, 340]]
      : f === 'square' ? [[cx - 96, 220], [cx - 30, 180], [cx + 70, 184], [cx + 112, 230], [cx + 116, 330], [cx + 110, 420], [cx + 70, 466], [cx - 40, 470], [cx - 92, 430], [cx - 102, 330]]
      : [[cx - 96, 250], [cx - 40, 186], [cx + 60, 188], [cx + 116, 250], [cx + 124, 340], [cx + 96, 430], [cx + 30, 474], [cx - 40, 466], [cx - 92, 420], [cx - 108, 340]];
    const Fw = F.map(p => [cx + (p[0] - cx) * w, p[1]]);
    fill(Fw, S); ctx.save(); ctx.beginPath(); spline(Fw); ctx.clip(); fill([[cx - 140, 220], [cx - 60, 240], [cx - 66, 420], [cx - 140, 460]], SH); ell(cx + 46, 360, 30, 18, 'rgba(230,110,90,.35)'); ctx.restore(); faceLight(Fw, cx + 30, 290); ink(Fw, 3, 7, INK, true);
    if (h.beard === 'stubble') { ctx.save(); ctx.beginPath(); spline(Fw); ctx.clip(); fill([[cx - 110, 380], [cx + 130, 380], [cx + 130, 520], [cx - 110, 520]], 'rgba(40,30,30,.22)'); ctx.restore(); }
    if (h.beard === 'full') shape([[cx - 96, 340], [cx - 80, 420], [cx - 30, 476], [cx + 30, 490], [cx + 90, 440], [cx + 116, 350], [cx + 90, 396], [cx + 40, 404], [cx - 10, 400], [cx - 60, 380]], HC, 2, 5);
    // hair
    const hs = h.hair || 'short';
    if (hs === 'short' || hs === 'long' || hs === 'bun') shape([[cx - 100, 300], [cx - 108, 220], [cx - 60, 166], [cx + 20, 150], [cx + 100, 170], [cx + 122, 240], [cx + 80, 214], [cx + 20, 220], [cx - 40, 214], [cx - 76, 250]], HC, 3, 7);
    if (hs === 'bun') { ell(cx - 20, 130, 52, 46, HC, 4); }
    if (hs === 'spiky') { const P = [[cx - 100, 290]]; for (let i = 0; i < 9; i++) { const x = cx - 100 + i * 26; P.push([x + 13, 120 + (i % 2) * 20], [x + 26, 205]); } P.push([cx + 124, 260]); shape(P, HC, 3, 6); }
    if (hs === 'bald' || hs === 'afro') { ell(cx + 10, 205, 40, 12, 'rgba(255,255,255,.35)', 0, -0.2); if (hs === 'bald') ink([[cx - 104, 300], [cx - 96, 250]], 2, 6, HC); }
    if (hs === 'cap') { shape([[cx - 104, 250], [cx - 96, 180], [cx - 30, 140], [cx + 60, 142], [cx + 112, 190], [cx + 116, 240]], h.capCol || '#1d4ed8', 3, 6); shape([[cx + 60, 236], [cx + 200, 240], [cx + 196, 262], [cx + 60, 262]], h.capCol || '#1d4ed8', 3, 5); ell(cx + 10, 150, 14, 8, '#fff', 2); }
    if (hs === 'sunhat') { shape([[cx - 210, 240], [cx - 120, 200], [cx - 90, 120], [cx + 10, 90], [cx + 110, 120], [cx + 140, 200], [cx + 230, 240], [cx + 120, 262], [cx - 100, 262]], h.capCol || '#f4d58d', 3, 6); fill([[cx - 100, 200], [cx + 140, 200], [cx + 140, 222], [cx - 100, 222]], h.band || '#ff4d6d'); }
    // brows + eyes
    const bu = expr === 'shock' ? -12 : 0, bt = expr === 'angry' ? 0.3 : (expr === 'sad' || expr === 'cry') ? -0.25 : 0;
    brow(cx - 36, 262 + bu, cx + 24, 262 + bu, HC === '#f2f2f2' ? '#9a9a9a' : HC, bt); brow(cx + 46, 260 + bu, cx + 100, 260 + bu, HC === '#f2f2f2' ? '#9a9a9a' : HC, -bt);
    for (const ex of [cx - 6, cx + 72]) eye(ex, 294, 15, 10, h.iris || '#5a3a1e', expr === 'cry' ? 'happy' : expr);
    if (h.glasses === 'sun') { for (const ex of [cx - 6, cx + 72]) ell(ex, 294, 34, 22, '#111', 3); ink([[cx + 26, 290], [cx + 40, 290]], 3, 4); ell(cx - 16, 286, 10, 5, 'rgba(255,255,255,.5)'); }
    if (h.glasses === 'round') { for (const ex of [cx - 6, cx + 72]) { ctx.beginPath(); ctx.arc(ex, 294, 30, 0, Math.PI * 2); ctx.lineWidth = 6; ctx.strokeStyle = INK; ctx.stroke(); } }
    // nose
    const ns = h.nose || 1; shape([[cx + 34, 300], [cx + 34 + 18 * ns, 340], [cx + 40 + 34 * ns, 352 + 6 * ns], [cx + 34 + 22 * ns, 372], [cx + 30, 364]], S, 2, 5);
    if (h.beard === 'mustache') shape([[cx - 6, 392], [cx + 40, 380], [cx + 90, 392], [cx + 80, 406], [cx + 40, 398], [cx, 408]], HC, 2, 4);
    // mouth
    const my = 416, mc = h.lips || '#6a1a14';
    if (expr === 'cry') { wail(cx + 40, my - 6, 44, 48); tears(cx + 32, 294, window.T2T || 0); }
    else if (expr === 'shock') ell(cx + 40, my + 8, 18, 26, '#5a1010', 4);
    else if (expr === 'sad') ink([[cx + 8, my + 8], [cx + 40, my - 2], [cx + 72, my + 8]], 3, 6);
    else if (expr === 'sleep') ell(cx + 40, my + 4, 12, 9, '#5a1010', 3);
    else if (expr === 'angry') { const M = [[cx, my - 4], [cx + 80, my - 6], [cx + 76, my + 20], [cx + 4, my + 22]]; fill(M, '#fffdf6'); ink([[cx + 2, my + 8], [cx + 78, my + 7]], 1, 3); ink(M, 3, 6, INK, true); }
    else { const big = expr === 'grin' ? 1.4 : 1; const M = [[cx + 4, my - 8], [cx + 40, my - 12], [cx + 80, my - 8], [cx + 66, my + 18 * big], [cx + 40, my + 26 * big], [cx + 14, my + 18 * big]]; fill(M, mc); ctx.save(); ctx.beginPath(); spline(M); ctx.clip(); fill([[cx - 10, my - 20], [cx + 90, my - 20], [cx + 90, my + 2], [cx - 10, my + 2]], '#fff'); ctx.restore(); ink(M, 2, 5, INK, true); }
    if (h.earring) ell(cx - 100, 380, 9, 9, '#ffd60a', 3);
  }
  // ---------------- characters ----------------
  const RONALDO = { cx: 300, shoulder: 108, waist: 58, leg: 360, arm: 300, skin: '#c98a5e', shade: '#a96d45', num: '7', abs: true,
    kit: { shirt: '#d0101a', collar: '#0b6e35', shorts: '#0b5e2f', sock: '#d0101a', sockShade: '#9e0c14', boot: '#ff5a1f', num: '#ffffff' } };
  const MESSI = { cx: 300, shoulder: 92, waist: 56, leg: 300, arm: 270, skin: '#e6b38d', shade: '#c8916b', num: '10',
    kit: { shirt: '#ffffff', stripes: '#75aadb', collar: '#1b2a4a', shorts: '#1b1b1b', sock: '#ffffff', sockShade: '#cfd8e3', boot: '#ffd21f', num: '#1b2a4a' } };
  const POSES = {
    hips: { lArm: [-30, 60], rArm: [30, -60], lLeg: [-6, 2], rLeg: [8, -2], hands: { l: 'fist', r: 'fist' } },
    siu: { lArm: [-40, -20], rArm: [40, 20], lLeg: [-18, -10], rLeg: [18, 10], hands: { l: 'open', r: 'open' } },
    sky: { lArm: [-160, -175], rArm: [160, 175], lLeg: [-4, 0], rLeg: [6, 0], hands: { l: 'point', r: 'point' } },
    cry: { lArm: [-145, 165], rArm: [145, -165], lLeg: [-30, -14], rLeg: [30, 14], hands: { l: 'open', r: 'open' } },
    run1: { lArm: [40, 100], rArm: [-40, -10], lLeg: [-35, 10], rLeg: [35, -60], hands: { l: 'fist', r: 'fist' } },
    run2: { lArm: [-40, -10], rArm: [40, 100], lLeg: [35, -60], rLeg: [-35, 10], hands: { l: 'fist', r: 'fist' } },
    kick: { lArm: [-70, -30], rArm: [50, 10], lLeg: [-4, 0], rLeg: [60, 95], hands: { l: 'open', r: 'fist' } },
    shock: { lArm: [-95, 178], rArm: [95, -178], lLeg: [-10, -4], rLeg: [10, 4], hands: { l: 'open', r: 'open' } },
    sad: { lArm: [-8, 10], rArm: [8, -10], lLeg: [-4, 0], rLeg: [4, 0], hands: {} },
  };
  function mix(a, b, k) { a = POSES[a] || a; b = POSES[b] || b; const o = { hands: k < 0.5 ? a.hands : b.hands };
    for (const key of ['lArm', 'rArm', 'lLeg', 'rLeg']) o[key] = [0, 1].map(i => a[key][i] + (b[key][i] - a[key][i]) * k); return o; }
  window.toon2 = { mix, POSES,
    draw(c2d, who, pose, expr, x, y, s, kit) {
      ctx = c2d; ctx.save(); ctx.translate(x, y); ctx.rotate(window.T2LEAN || 0); ctx.scale(s, s); ctx.translate(-300, -1260); ctx.lineJoin = 'round';
      const c0 = typeof who === 'object' ? Object.assign({ cx: 300, shoulder: 96, waist: 60, leg: 300, arm: 270, num: '', abs: false }, who) : who === 'ronaldo' ? RONALDO : MESSI; const c = kit ? Object.assign({}, c0, { kit: Object.assign({}, c0.kit, kit), num: kit.number ?? c0.num, abs: kit.abs ?? c0.abs }) : c0; 
      body(c, typeof pose === 'string' ? POSES[pose] : pose);
      if (typeof who === 'object') { const hs = (who.head || {}).scale || 1.1; ctx.save(); ctx.translate(300, 590); ctx.scale(hs, hs); ctx.translate(-300, -590); headGeneric(c.cx, expr, who.head || {}, c); ctx.restore(); }
      else if (who === 'ronaldo') headRonaldo(c.cx, expr); else { ctx.save(); ctx.translate(300, 590); ctx.scale(1.12, 1.12); ctx.translate(-300, -590); headMessi(c.cx, expr); ctx.restore(); }
      ctx.restore();
    }
  };
})();
