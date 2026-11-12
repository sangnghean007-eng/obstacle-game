// Neymar Jr. caricature in the style of the reference Short (editorial football caricature):
// strong exaggeration (long face & neck, big nose with red tip, big toothy grin), clean flat colour,
// rosy patches, solid hair/beard shapes with a few inner lines, dark-brown ink. Pure vector, no photo pixels.
// Proportions come from the traced reference photo landmarks (see neymar_vector.js), then exaggerated.
(function () {
  const C = {
    line: '#3b1d10', skin: '#e0a47c', skin2: '#c9845d', rose: 'rgba(232,92,92,0.2)', nose: 'rgba(232,120,105,0.55)',
    hair: '#24160e', hair2: '#4b3020', tip: '#e2b459', beard: '#4e3020', beard2: '#6a4430',
    lip: '#c06a5c', lip2: '#a0544a', teeth: '#fffdf6', gum: '#7a1f1f', white: '#ffffff', iris: '#3a2516', tattoo: '#3b2b3b',
  };
  const TAU = Math.PI * 2;
  function rng(seed) { return () => (seed = (seed * 16807) % 2147483647, (seed - 1) / 2147483646); }
  function spline(ctx, pts, closed) {
    const n = pts.length, P = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < (closed ? n : n - 1); i++) {
      const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
      ctx.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]);
    }
    if (closed) ctx.closePath();
  }
  function shape(ctx, pts, fill, stroke, lw = 5, closed = true) {
    ctx.beginPath(); spline(ctx, pts, closed);
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); }
  }
  const line = (ctx, pts, col, lw) => shape(ctx, pts, null, col, lw, false);
  function ell(ctx, x, y, rx, ry, fill, stroke, lw = 4, rot = 0) {
    ctx.beginPath(); ctx.ellipse(x, y, rx, ry, rot, 0, TAU);
    if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); }
  }
  const mirror = pts => pts.map(([x, y]) => [600 - x, y]);

  // ---------------- shapes (design space: x 0..600, y 0..1080) ----------------
  const FACE = [[300, 228], [390, 236], [448, 278], [468, 340], [470, 410], [458, 480], [432, 560], [394, 640], [348, 712], [300, 742], [252, 712], [206, 640], [168, 560], [142, 480], [130, 410], [132, 340], [152, 278], [210, 236]];
  const NECK = [[236, 640], [232, 760], [226, 900], [220, 1080], [380, 1080], [374, 900], [368, 760], [364, 640]];
  const EAR = [[132, 352], [100, 340], [76, 362], [72, 404], [80, 446], [96, 478], [118, 488], [136, 470]];
  const BEARD = [[124, 430], [134, 500], [160, 576], [204, 652], [252, 708], [300, 732], [348, 708], [396, 652], [440, 576], [466, 500], [476, 430], [462, 470], [440, 540], [404, 600], [372, 612], [356, 650], [300, 668], [244, 650], [228, 612], [196, 600], [160, 540], [138, 470]];
  const MUST = [[214, 568], [250, 552], [300, 556], [350, 552], [386, 568], [376, 576], [340, 568], [300, 572], [260, 568], [224, 576]];
  const HAIRLINE_Y = 262;

  function hair(ctx, t) {
    const R = rng(7);
    // back mass (silhouette): wide curly mop, a bit taller than real for caricature
    const MASS = [[300, 92], [372, 98], [432, 122], [478, 160], [504, 210], [512, 266], [506, 322], [490, 372], [470, 350], [458, 312], [430, 290], [380, 280], [330, 290], [300, 278], [262, 292], [214, 282], [168, 292], [142, 314], [130, 350], [110, 372], [94, 322], [88, 266], [96, 210], [122, 160], [168, 122], [228, 98]];
    shape(ctx, MASS, C.hair, C.line, 6);
    // curly locks: hook-shaped tufts, back to front; blond tips (2018 look)
    const locks = [];
    const mp = new Path2D(); mp.moveTo(MASS[0][0], MASS[0][1]); MASS.forEach(q => mp.lineTo(q[0], q[1])); mp.closePath();
    const M = ctx.getTransform();
    for (let i = 0; i < 900 && locks.length < 95; i++) {
      const x = 90 + R() * 420, y = 90 + R() * 290, d = M.transformPoint(new DOMPoint(x, y));
      if (!ctx.isPointInPath(mp, d.x, d.y)) continue;
      locks.push([x, y, 20 + R() * 12, R() * TAU, R()]);
    }
    locks.sort((p, q) => p[1] - q[1]);
    for (const [x, y, r, a, v] of locks) {
      ctx.save(); ctx.translate(x, y); ctx.rotate(a);
      ctx.beginPath(); ctx.moveTo(-r * 0.6, r * 0.2);
      ctx.bezierCurveTo(-r * 0.8, -r * 0.9, r * 0.9, -r * 0.9, r * 0.7, r * 0.1);
      ctx.bezierCurveTo(r * 0.55, r * 0.6, -r * 0.05, r * 0.55, 0, r * 0.05);
      ctx.bezierCurveTo(r * 0.05, -r * 0.25, r * 0.4, -r * 0.2, r * 0.32, r * 0.1);
      ctx.fillStyle = C.hair; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 3.5; ctx.lineJoin = 'round'; ctx.stroke();
      ctx.beginPath(); ctx.arc(0, -r * 0.05, r * 0.5, Math.PI * 1.05, Math.PI * 1.75);
      ctx.strokeStyle = v < 0.45 ? C.tip : C.hair2; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.stroke();
      ctx.restore();
    }
    // a few locks falling on the forehead
    for (const [x, y, s] of [[262, 296, 1], [330, 300, -1], [196, 300, 1], [404, 298, -1]]) {
      ctx.save(); ctx.translate(x, y); ctx.scale(s, 1);
      shape(ctx, [[-14, -20], [12, -24], [20, 0], [8, 22], [-6, 30], [-2, 12], [6, 2], [-10, -2]], C.hair, C.line, 3.5);
      line(ctx, [[2, -14], [10, 0], [2, 14]], C.tip, 4);
      ctx.restore();
    }
  }

  function eye(ctx, cx, cy, side, f, t, look) {
    if (f === 'pain' || (f === 'wink' && side < 0)) {
      line(ctx, [[cx - 32, cy - 2], [cx, cy + 8], [cx + 32, cy - 2]], C.line, 6);
      line(ctx, [[cx + side * 36, cy - 10], [cx + side * 48, cy - 16]], C.line, 3); line(ctx, [[cx + side * 38, cy + 2], [cx + side * 50, cy + 2]], C.line, 3);
      return;
    }
    const open = f === 'shock' ? 24 : f === 'grin' ? 9 : 11;
    const inner = cx - side * 30, outer = cx + side * 34;
    const up = [[inner, cy + 2], [cx - side * 10, cy - open], [cx + side * 14, cy - open + 2], [outer, cy + 4]];
    const lo = [[outer, cy + 4], [cx + side * 6, cy + (f === 'shock' ? 22 : 12)], [inner, cy + 2]];
    ctx.save(); ctx.beginPath(); spline(ctx, up, false); spline(ctx, lo.slice(0), false); ctx.closePath();
    ctx.fillStyle = C.white; ctx.fill(); ctx.clip();
    const lx = look ? look[0] : 0, ly = look ? look[1] : 0;
    ell(ctx, cx + lx, cy + 1 + ly, f === 'shock' ? 8 : 12, f === 'shock' ? 8 : 12, C.iris, null);
    ell(ctx, cx + lx - 3, cy - 3 + ly, 3, 3, '#fff', null);
    ctx.restore();
    line(ctx, up, C.line, 6); line(ctx, lo, C.line, 2.5);
    line(ctx, [[cx - side * 22, cy - open - 6], [cx + side * 4, cy - open - 10], [cx + side * 26, cy - open - 4]], 'rgba(59,29,16,.55)', 2.5); // lid crease
    line(ctx, [[cx - side * 18, cy + 22], [cx + side * 18, cy + 22]], 'rgba(59,29,16,.35)', 2.5);                                         // under-eye
  }

  function mouth(ctx, f, t) {
    if (f === 'grin' || f === 'smug') {
      const w = f === 'grin' ? 108 : 96, h = f === 'grin' ? 58 : 44;
      const M = [[300 - w, 574], [300 - w * 0.5, 584], [300, 586], [300 + w * 0.5, 584], [300 + w, 574], [300 + w * 0.6, 588 + h * 0.75], [300, 588 + h], [300 - w * 0.6, 588 + h * 0.75]];
      line(ctx, [[232, 520], [206, 556], [196, 590]], 'rgba(59,29,16,.6)', 3.5); line(ctx, [[368, 520], [394, 556], [404, 590]], 'rgba(59,29,16,.6)', 3.5);
      shape(ctx, M, C.gum, null);
      ctx.save(); ctx.beginPath(); spline(ctx, M, true); ctx.clip();
      ctx.fillStyle = C.teeth; ctx.fillRect(300 - w, 560, w * 2, 44 + h * 0.15);            // big upper teeth (Neymar's trademark grin)
      ctx.strokeStyle = 'rgba(60,30,20,.45)'; ctx.lineWidth = 2.5;
      [-0.62, -0.38, -0.16, 0, 0.16, 0.38, 0.62].forEach(k => { ctx.beginPath(); ctx.moveTo(300 + k * w, 572); ctx.lineTo(300 + k * w * 1.02, 598 + h * 0.15 - Math.abs(k) * 12); ctx.stroke(); });
      ctx.fillStyle = '#f2ece2'; ctx.fillRect(300 - w * 0.45, 590 + h * 0.62, w * 0.9, 12);
      ctx.restore();
      shape(ctx, M, null, C.line, 5);
      line(ctx, [[300 - w * 0.55, 592 + h * 0.95], [300, 600 + h], [300 + w * 0.55, 592 + h * 0.95]], C.lip, 7);   // lower lip
      line(ctx, [[300 - w - 8, 566], [300 - w + 2, 580]], C.line, 3.5); line(ctx, [[300 + w + 8, 566], [300 + w - 2, 580]], C.line, 3.5);
    } else if (f === 'pain' || f === 'shock') {
      const w = f === 'pain' ? 74 : 38, h = f === 'pain' ? 92 + Math.sin(t * 30) * 8 : 60;
      const M = f === 'pain' ? [[300 - w, 610], [300 - w * 0.5, 576], [300, 570], [300 + w * 0.5, 576], [300 + w, 610], [300 + w * 0.7, 570 + h], [300, 585 + h], [300 - w * 0.7, 570 + h]]
                             : [[300 - w, 600], [300, 574], [300 + w, 600], [300 + w * 0.8, 574 + h], [300, 584 + h], [300 - w * 0.8, 574 + h]];
      shape(ctx, M, C.gum, null);
      ctx.save(); ctx.beginPath(); spline(ctx, M, true); ctx.clip();
      ctx.fillStyle = C.teeth; ctx.fillRect(300 - w, 560, w * 2, 30);
      ell(ctx, 300, 570 + h * 0.85, w * 0.6, h * 0.28, '#d9585c', null);
      ctx.restore(); shape(ctx, M, null, C.line, 5);
    } else { // neutral: full lips, slight pout (like the reference photo)
      shape(ctx, [[214, 596], [246, 580], [276, 576], [300, 582], [326, 576], [356, 580], [386, 596], [300, 602]], C.lip2, C.line, 4);
      shape(ctx, [[216, 598], [300, 604], [384, 598], [362, 628], [300, 644], [238, 628]], C.lip, C.line, 4);
      ell(ctx, 300, 620, 30, 6, 'rgba(255,220,210,.6)', null);
    }
  }

  function drawNeymarH(ctx, o = {}) {
    const f = o.face || 'grin', t = o.t || 0;
    ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    // neck (long, as in the reference style) + script tattoo
    shape(ctx, NECK, C.skin, C.line, 5);
    shape(ctx, [[232, 650], [300, 730], [368, 650], [370, 720], [300, 790], [230, 720]], C.skin2, null);
    line(ctx, [[338, 790], [350, 812], [342, 836], [356, 860], [348, 884]], C.tattoo, 3); line(ctx, [[356, 798], [364, 822], [358, 846]], C.tattoo, 2.5);
    // ears + diamond stud
    shape(ctx, EAR, C.skin, C.line, 5); shape(ctx, mirror(EAR), C.skin, C.line, 5);
    line(ctx, [[118, 372], [96, 388], [96, 430], [110, 456]], C.skin2, 7); line(ctx, [[482, 372], [504, 388], [504, 430], [490, 456]], C.skin2, 7);
    ell(ctx, 476, 470, 6, 6, '#eef8ff', C.line, 2.5);
    // face
    shape(ctx, FACE, C.skin, null);
    ctx.save(); ctx.beginPath(); spline(ctx, FACE, true); ctx.clip();
    shape(ctx, [[126, 330], [170, 360], [160, 470], [150, 560], [120, 470]], C.skin2, null);         // side planes
    shape(ctx, [[474, 330], [430, 360], [440, 470], [450, 560], [480, 470]], C.skin2, null);
    shape(ctx, [[278, 372], [282, 450], [270, 486], [262, 470], [270, 420]], C.skin2, null);        // nose side
    ell(ctx, 300, 548, 70, 12, C.skin2, null);                                                       // under nose
    ell(ctx, 172, 470, 48, 30, C.rose, null); ell(ctx, 428, 470, 48, 30, C.rose, null);              // rosy cheeks
    ell(ctx, 300, 300, 70, 22, 'rgba(232,92,92,0.16)', null);                                        // rosy forehead
    // beard: solid chinstrap + goatee + thin mustache, a few hair strokes
    shape(ctx, BEARD, C.beard, null);
    shape(ctx, MUST, C.beard, null);
    { const R = rng(3); ctx.strokeStyle = C.beard2; ctx.lineWidth = 2.5;
      for (let i = 0; i < 70; i++) { const a = R() * Math.PI, rr = 0.75 + R() * 0.25, x = 300 + Math.cos(a) * 170 * rr, y = 470 + Math.sin(a) * 250 * rr;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + (R() - 0.5) * 6, y + 10); ctx.stroke(); } }
    ctx.restore();
    shape(ctx, FACE.slice(3, 16), null, C.line, 6, false);
    // mouth (over the beard)
    mouth(ctx, f, t);
    // nose: long bridge, wide flared base, round red tip
    line(ctx, [[282, 372], [280, 430], [272, 476]], C.line, 3.5);
    ell(ctx, 300, 498, 38, 34, C.skin, null);
    ell(ctx, 300, 502, 26, 20, C.nose, null);
    shape(ctx, [[256, 486], [232, 498], [228, 522], [246, 536], [268, 532]], C.skin, C.line, 4.5, false);
    shape(ctx, [[344, 486], [368, 498], [372, 522], [354, 536], [332, 532]], C.skin, C.line, 4.5, false);
    line(ctx, [[268, 532], [284, 540], [300, 542], [316, 540], [332, 532]], C.line, 4);
    ell(ctx, 262, 528, 11, 6, '#3b1d12', null, 0, 0.3); ell(ctx, 338, 528, 11, 6, '#3b1d12', null, 0, -0.3);
    ell(ctx, 308, 486, 10, 7, 'rgba(255,240,230,.85)', null);
    // eyes + thick straight brows close to the eyes
    eye(ctx, 234, 392, -1, f, t, o.look); eye(ctx, 366, 392, 1, f, t, o.look);
    const lift0 = 18; const lift = f === 'pain' ? -18 : f === 'shock' ? -14 : f === 'angry' ? 8 : 0;
    const BR = [[278, 364 + lift * 0.4], [272, 346 + lift], [226, 340 + lift * 0.6], [186, 344], [164, 360], [172, 368], [206, 360], [242, 360 + lift * 0.5], [274, 372 + lift * 0.3]];
    shape(ctx, BR, C.hair, C.line, 2.5); shape(ctx, mirror(BR), C.hair, C.line, 2.5);
    if (f === 'pain') for (const [x, d] of [[234, -1], [366, 1]]) for (let i = 0; i < 9; i++) { const k = ((t * 2.5 + i / 9) % 1); ell(ctx, x + d * k * 260, 384 - k * 110 + k * k * 380, 11, 15, '#7fd3ff', '#1f6fb0', 3); }
    // hair on top
    hair(ctx, t);
    ctx.restore();
  }
  window.drawNeymarH = drawNeymarH;
})();
