// Neymar Jr. caricature in a hand-drawn editorial-cartoon style (flat colour, one shadow tone,
// brown variable ink, pink blush). Every landmark below was traced from the CC BY-SA reference photo
// "20180610 FIFA Friendly Match Austria vs. Brazil Neymar 850 1705.jpg" (Granada, Wikimedia Commons)
// in a 600x840 "grid" space, then pushed through a caricature transform (bigger hair, nose, mouth; longer chin).
(function () {
  const C = {
    line: '#3a1c0f', skin: '#d8946a', shade: '#b57250', light: '#eaae84', blush: 'rgba(226,96,86,0.26)',
    hair: '#21140d', hair2: '#4a2e1e', tip: '#d4a24a', beard: 'rgba(82,50,32,0.34)', beard2: 'rgba(52,30,18,0.5)',
    lipU: '#9a4d43', lipL: '#c7776a', lipHi: '#e3a196', white: '#fbf6ef', iris: '#5a3820', tattoo: 'rgba(40,30,40,.75)',
  };
  // ---------- caricature transform (grid space) ----------
  function bulge(p, c, r, s) {
    const dx = p[0] - c[0], dy = p[1] - c[1], d2 = (dx * dx + dy * dy) / (r * r);
    if (d2 >= 1) return p; const f = 1 + s * (1 - d2) * (1 - d2); return [c[0] + dx * f, c[1] + dy * f];
  }
  function T(p, ex) {
    let [x, y] = p;
    if (y < 380) { const k = Math.min(1, (380 - y) / 330); y = 380 - (380 - y) * (1 + 0.14 * ex * k); x = 290 + (x - 290) * (1 + 0.05 * ex * k); }
    if (y > 590) { const k = Math.min(1, (y - 590) / 210); y = 590 + (y - 590) * (1 + 0.16 * ex * k); x = 290 + (x - 290) * (1 - 0.10 * ex * k); }
    let q = [x, y];
    q = bulge(q, [290, 525], 95, 0.32 * ex);   // nose
    q = bulge(q, [292, 622], 115, 0.22 * ex);  // mouth
    q = bulge(q, [172, 425], 60, 0.12 * ex); q = bulge(q, [348, 418], 60, 0.12 * ex);
    return q;
  }
  // ---------- path helpers ----------
  function spline(ctx, pts, closed) { // Catmull-Rom -> Bezier
    const n = pts.length; if (n < 2) return;
    const P = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
    ctx.moveTo(pts[0][0], pts[0][1]);
    const last = closed ? n : n - 1;
    for (let i = 0; i < last; i++) {
      const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
      ctx.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]);
    }
    if (closed) ctx.closePath();
  }
  function rng(seed) { return () => (seed = (seed * 16807) % 2147483647, (seed - 1) / 2147483646); }

  function drawNeymar(ctx, o = {}) {
    const ex = o.ex ?? 1, face = o.face || 'neutral', t = o.t || 0;
    const tp = pts => pts.map(p => T(p, ex));
    const shape = (pts, fill, stroke, lw, closed = true) => { ctx.beginPath(); spline(ctx, tp(pts), closed); if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); } };
    const line = (pts, col, lw) => shape(pts, null, col, lw, false);
    const ellipse = (c, rx, ry, fill, stroke, lw, rot = 0) => { const q = T(c, ex); ctx.beginPath(); ctx.ellipse(q[0], q[1], rx, ry, rot, 0, Math.PI * 2); if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); } };
    ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round';

    // ---------- shoulders + jersey (yellow, green collar, no crest/logos) ----------
    if (o.bust) {
      const SH = [[176, 830], [100, 860], [30, 900], [-20, 980], [-30, 1080], [620, 1080], [610, 980], [560, 900], [490, 860], [412, 830]];
      shape(SH, '#ffd400', C.line, 5);
      shape([[40, 920], [10, 990], [0, 1080], [80, 1080], [90, 990]], '#e8b800', null);
      shape([[548, 920], [578, 990], [588, 1080], [508, 1080], [498, 990]], '#e8b800', null);
      shape([[176, 828], [230, 880], [300, 900], [360, 880], [412, 828], [420, 846], [362, 904], [300, 924], [226, 904], [168, 846]], '#109a4a', C.line, 4);
      if (o.num !== false) { ctx.save(); const q = T([300, 1000], 0); ctx.font = '900 70px Inter, sans-serif'; ctx.textAlign = 'center'; ctx.fillStyle = '#109a4a'; ctx.fillText('10', q[0] + 150, q[1]); ctx.restore(); }
    }
    // ---------- neck + tattoo ----------
    const NECK = [[185, 700], [182, 780], [176, 860], [412, 860], [406, 780], [404, 700]];
    shape(NECK, C.skin, C.line, 5);
    shape([[185, 740], [300, 820], [406, 740], [408, 790], [300, 850], [182, 790]], C.shade, null);
    ctx.save(); ctx.strokeStyle = C.tattoo; ctx.lineWidth = 2.2;
    line([[418, 742], [428, 760], [420, 778], [432, 792], [426, 810], [438, 826]], C.tattoo, 2.2);
    line([[436, 748], [444, 768], [436, 786], [446, 802]], C.tattoo, 2);
    ctx.restore();

    // ---------- ears ----------
    const EAR_L = [[104, 418], [82, 412], [62, 432], [56, 470], [61, 512], [70, 552], [80, 582], [94, 594], [108, 586], [110, 540]];
    const EAR_R = [[480, 414], [506, 404], [532, 412], [553, 440], [561, 480], [557, 522], [546, 562], [531, 588], [514, 594], [494, 582], [484, 540]];
    shape(EAR_L, C.skin, C.line, 5); shape(EAR_R, C.skin, C.line, 5);
    line([[96, 440], [78, 452], [76, 492], [84, 530], [96, 552]], C.shade, 7); line([[92, 470], [86, 500], [94, 530]], C.line, 3);
    line([[490, 436], [520, 434], [538, 466], [536, 512], [524, 548]], C.shade, 7); line([[502, 462], [522, 476], [520, 520], [510, 540]], C.line, 3);
    ellipse([521, 552], 5, 5, '#f2f7ff', C.line, 2); // stud

    // ---------- face ----------
    const FACE = [[95, 330], [100, 400], [100, 470], [100, 560], [110, 622], [130, 682], [165, 732], [215, 772], [270, 796], [300, 799], [345, 791], [400, 766], [440, 726], [470, 670], [478, 600], [482, 520], [485, 450], [480, 380], [470, 300], [400, 250], [290, 232], [180, 250], [110, 300]];
    shape(FACE, C.skin, null);
    // shadows
    ctx.save(); ctx.beginPath(); spline(ctx, tp(FACE), true); ctx.clip();
    shape([[100, 300], [140, 330], [130, 420], [112, 520], [100, 560], [90, 400]], C.shade, null);                 // left temple/cheek
    shape([[480, 300], [450, 330], [458, 420], [470, 520], [482, 560], [492, 400]], C.shade, null);
    shape([[112, 404], [170, 394], [230, 404], [226, 414], [170, 410], [118, 416]], C.shade, null);                // eye sockets
    shape([[300, 398], [350, 388], [458, 398], [452, 410], [350, 404], [304, 410]], C.shade, null);
    shape([[264, 420], [270, 470], [264, 508], [246, 522], [236, 506], [252, 472], [256, 430]], C.shade, null);   // nose side
    ellipse([290, 566], 50, 11, C.shade, null);                                                                      // under nose
    ctx.globalAlpha = 0.55; ellipse([165, 470], 34, 14, C.light, null, 0, -0.2); ellipse([405, 463], 34, 14, C.light, null, 0, 0.2); ellipse([290, 305], 55, 18, C.light, null); ctx.globalAlpha = 1;
    ellipse([300, 452], 9, 30, C.light, null);                                                                       // nose bridge
    ctx.restore();
    // blush (style signature: pink nose + cheeks)
    ellipse([160, 500], 40, 20, C.blush, null); ellipse([420, 495], 40, 20, C.blush, null);

    // ---------- beard (solid mass + hair flicks) ----------
    const BEARD = [[105, 500], [100, 560], [110, 622], [130, 682], [165, 732], [215, 772], [270, 796], [300, 799], [345, 791], [400, 766], [440, 726], [470, 670], [478, 600], [481, 520], [479, 500], [462, 560], [428, 590], [388, 588], [370, 578], [330, 567], [290, 563], [250, 567], [210, 579], [180, 590], [138, 568], [114, 530]];
    shape(BEARD, C.beard, null);
    { const R = rng(4); const tb = tp(BEARD); ctx.strokeStyle = C.beard; ctx.lineWidth = 2.2;
      for (let i = 0; i < tb.length; i++) { const a = tb[i], b = tb[(i + 1) % tb.length];
        for (let j = 0; j < 7; j++) { const k = j / 7, x = a[0] + (b[0] - a[0]) * k, y = a[1] + (b[1] - a[1]) * k, nx = -(b[1] - a[1]), ny = b[0] - a[0], nl = Math.hypot(nx, ny) || 1;
          const L = 5 + R() * 7; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + nx / nl * L * (i < 14 && i > 0 ? 0.4 : 1) * -1, y + ny / nl * L * -1); ctx.stroke(); } }
      ctx.save(); ctx.beginPath(); spline(ctx, tb, true); ctx.clip(); ctx.strokeStyle = C.beard2; ctx.lineWidth = 2;
      for (let i = 0; i < 260; i++) { const x = 90 + R() * 400, y = 460 + R() * 350, q = T([x, y], ex); ctx.beginPath(); ctx.moveTo(q[0], q[1]); ctx.lineTo(q[0] + (R() - .5) * 5, q[1] + 6 + R() * 6); ctx.stroke(); }
      ctx.restore(); }
    // face contour ink (variable width feel: draw twice)
    shape(FACE.slice(2, 19), null, C.line, 6, false);

    // ---------- mouth ----------
    const open = face === 'pain' || face === 'shock' || face === 'grin';
    if (!open) {
      shape([[204, 616], [228, 600], [252, 594], [290, 599], [330, 594], [356, 600], [382, 613], [292, 621]], C.lipU, C.line, 3.5);
      shape([[206, 618], [292, 622], [380, 615], [362, 636], [292, 650], [226, 636]], C.lipL, C.line, 3.5);
      ellipse([292, 634], 30, 6, C.lipHi, null);
      line([[204, 617], [250, 619], [292, 623], [336, 619], [381, 614]], C.line, 4.5);
    } else {
      const h = face === 'pain' ? 70 + Math.sin(t * 30) * 6 : face === 'shock' ? 45 : 34;
      const w = face === 'shock' ? 55 : 100;
      const M = face === 'pain' ? [[292 - w * 0.75, 640], [292 - w * 0.4, 600], [292, 594], [292 + w * 0.4, 600], [292 + w * 0.75, 640], [292 + w * 0.5, 612 + h], [292, 622 + h], [292 - w * 0.5, 612 + h]] : [[292 - w, 612], [292, 596], [292 + w, 612], [292 + w * 0.6, 612 + h * 0.9], [292, 612 + h], [292 - w * 0.6, 612 + h * 0.9]];
      shape(M, '#4a0c0e', C.line, 5);
      ctx.save(); ctx.beginPath(); spline(ctx, tp(M), true); ctx.clip();
      if (face !== 'pain') shape([[292 - w, 600], [292 + w, 600], [292 + w, 628], [292, 640], [292 - w, 628]], '#ffffff', null);       // big upper teeth
      else shape([[292 - w, 600], [292 + w, 600], [292 + w * 0.8, 614], [292 - w * 0.8, 614]], '#ffffff', null);
      for (let i = -3; i <= 3; i++) line([[292 + i * w / 4, 600], [292 + i * w / 4, 634]], 'rgba(0,0,0,.25)', 2);
      if (face !== 'grin') ellipse([292, 612 + h * 0.8], w * 0.5, h * 0.3, '#d65a5f', null);
      ctx.restore();
    }

    // ---------- nose ----------
    shape([[262, 430], [262, 480], [250, 508], [232, 516], [224, 532], [236, 550], [258, 548], [276, 558], [292, 562], [308, 558], [326, 548], [348, 550], [358, 532], [350, 516], [332, 508], [322, 480], [320, 430]], C.skin, null);
    ellipse([292, 522], 28, 20, C.blush, null);
    line([[262, 432], [258, 482], [248, 506]], C.line, 3);
    line([[244, 512], [226, 522], [226, 542], [244, 552], [262, 549]], C.line, 4.5);
    line([[340, 512], [358, 522], [358, 542], [340, 552], [322, 549]], C.line, 4.5);
    line([[262, 549], [278, 558], [292, 561], [306, 558], [322, 549]], C.line, 3.5);
    ellipse([256, 545], 10, 5, '#3b1d12', null, 0, 0.25); ellipse([328, 545], 10, 5, '#3b1d12', null, 0, -0.25);
    ellipse([300, 503], 9, 6, 'rgba(255,240,225,.8)', null);

    // ---------- eyes (narrow, hooded) ----------
    const eye = (c, inner, outer, peak, low, look, closed) => {
      if (closed) { line([outer, [c[0], c[1] + 6], inner], C.line, 6); return; }
      const up = [outer, [(outer[0] + c[0]) / 2, peak + 3], [c[0], peak], [(inner[0] + c[0]) / 2, peak + 4], inner];
      const lo = [inner, [c[0], low], outer];
      ctx.save(); ctx.beginPath(); spline(ctx, tp(up), false); spline(ctx, tp(lo).slice(1), false); ctx.closePath();
      ctx.fillStyle = C.white; ctx.fill(); ctx.clip();
      const ic = T([c[0] + look[0], c[1] + look[1]], ex);
      ctx.beginPath(); ctx.arc(ic[0], ic[1], 16, 0, Math.PI * 2); ctx.fillStyle = C.iris; ctx.fill();
      ctx.beginPath(); ctx.arc(ic[0], ic[1], 7, 0, Math.PI * 2); ctx.fillStyle = '#120a06'; ctx.fill();
      ctx.beginPath(); ctx.arc(ic[0] - 4, ic[1] - 5, 3.5, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill();
      ctx.beginPath(); spline(ctx, tp(up.map(([x, y]) => [x, y + 7])), false); ctx.lineWidth = 14; ctx.strokeStyle = 'rgba(120,70,45,.35)'; ctx.stroke(); // lid shadow
      ctx.restore();
      line(up, C.line, 8); line(lo, C.line, 2.5);
      line(up.slice(1, 4).map(([x, y]) => [x, y - 9]), 'rgba(58,28,15,.6)', 2.5);   // crease
    };
    line([[140, 446], [172, 452], [204, 446]], 'rgba(120,64,40,.55)', 2.5); line([[318, 440], [350, 446], [384, 438]], 'rgba(120,64,40,.55)', 2.5);
    const shock = face === 'shock';
    eye([172, 428], [212, 428], [128, 424], shock ? 400 : 412, shock ? 452 : 438, o.look || [2, 0], face === 'pain' || face === 'wink');
    eye([348, 420], [310, 422], [394, 416], shock ? 392 : 404, shock ? 446 : 430, o.look || [-2, 0], face === 'pain');

    if (face === 'pain') { // fountain tears
      for (const [ex0, d] of [[160, -1], [360, 1]]) for (let i = 0; i < 9; i++) { const k = ((t * 2.5 + i / 9) % 1), q = T([ex0, 440], ex);
        ctx.beginPath(); ctx.ellipse(q[0] + d * k * 260, q[1] - k * 120 + k * k * 380, 11, 15, 0, 0, Math.PI * 2); ctx.fillStyle = '#7fd3ff'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#1f6fb0'; ctx.stroke(); } }
    // ---------- brows (thick, straight, close to the eyes) ----------
    const lift = face === 'pain' ? -22 : face === 'shock' ? -14 : face === 'angry' ? 8 : 0;
    shape([[230, 392 + lift * 0.3], [225, 376 + lift], [180, 368 + lift * 0.6], [140, 374], [108, 390], [114, 398], [150, 388], [190, 384 + lift * 0.5], [228, 396 + lift * 0.3]], C.hair, C.line, 2);
    shape([[318, 382 + lift * 0.3], [328, 366 + lift], [380, 358 + lift * 0.6], [422, 362], [458, 376], [452, 386], [410, 378], [370, 375 + lift * 0.5], [328, 386 + lift * 0.3]], C.hair, C.line, 2);

    // ---------- hair: curly mass with scalloped outline, curls and blond tips ----------
    const HAIR = [[250, 42], [310, 40], [360, 52], [405, 70], [452, 108], [490, 150], [522, 200], [546, 250], [560, 300], [560, 342], [546, 382], [522, 412], [486, 424], [470, 400], [460, 340], [450, 300], [430, 280], [400, 262], [350, 248], [300, 240], [262, 244], [240, 266], [228, 250], [190, 255], [140, 280], [115, 320], [110, 380], [98, 412], [66, 432], [44, 400], [30, 350], [30, 300], [44, 250], [70, 200], [100, 150], [150, 100], [200, 62]];
    const th = tp(HAIR);
    // base mass
    ctx.beginPath(); spline(ctx, th, true); ctx.fillStyle = C.hair; ctx.fill();
    // curl clumps: sampled inside the silhouette, drawn back-to-front, each with ink rim + highlight arcs
    { const R = rng(31), blobs = []; const path = new Path2D(); { const c2 = path; c2.moveTo(th[0][0], th[0][1]); th.forEach(q => c2.lineTo(q[0], q[1])); c2.closePath(); }
      for (let i = 0; i < 2600 && blobs.length < 120; i++) { const x = 20 + R() * 560, y = 30 + R() * 420, q = T([x, y], ex), m = ctx.getTransform(), d = m.transformPoint(new DOMPoint(q[0], q[1])); if (ctx.isPointInPath(path, d.x, d.y)) blobs.push([q[0], q[1], 15 + R() * 12, R()]); }
      blobs.sort((a, b) => a[1] - b[1]);
      for (const [x, y, r, v] of blobs) {
        ctx.beginPath(); for (let k = 0; k <= 10; k++) { const a = k / 10 * Math.PI * 2, rr = r * (0.88 + 0.12 * Math.sin(a * 3 + v * 9)); ctx[k ? 'lineTo' : 'moveTo'](x + Math.cos(a) * rr, y + Math.sin(a) * rr); }
        ctx.closePath(); ctx.fillStyle = C.hair; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 2.5; ctx.stroke();
        ctx.beginPath(); ctx.arc(x - 1, y + 1, r * 0.62, Math.PI * (0.9 + v * 0.3), Math.PI * (2.0 + v * 0.3)); ctx.lineWidth = 3.5; ctx.strokeStyle = C.hair2; ctx.stroke();
        if (v < 0.45) { ctx.beginPath(); ctx.arc(x - 2, y, r * 0.6, Math.PI * 1.15, Math.PI * 1.55); ctx.lineWidth = 3.5; ctx.strokeStyle = C.tip; ctx.stroke(); }
      } }
    // outer ink around the whole hair silhouette (soft, behind clumps already drawn)
    ctx.restore();
  }
  window.drawNeymar = drawNeymar; window.NEY_T = T;
})();
