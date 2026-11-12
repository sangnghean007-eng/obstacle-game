// Neymar Jr. caricature in a hand-drawn editorial-cartoon style (flat colour, one shadow tone,
// brown variable ink, pink blush). Every landmark below was traced from the CC BY-SA reference photo
// "20180610 FIFA Friendly Match Austria vs. Brazil Neymar 850 1705.jpg" (Granada, Wikimedia Commons)
// in a 600x840 "grid" space, then pushed through a caricature transform (bigger hair, nose, mouth; longer chin).
(function () {
  const C = {
    line: '#3a1c0f', skin: '#d39468', shade: '#b57250', light: '#eaae84', blush: 'rgba(226,96,86,0.13)',
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
    if (y < 380) { const k = Math.min(1, (380 - y) / 330); y = 380 - (380 - y) * (1 + 0.05 * ex * k); x = 290 + (x - 290) * (1 + 0.03 * ex * k); }
    if (y > 590) { const k = Math.min(1, (y - 590) / 210); y = 590 + (y - 590) * (1 + 0.10 * ex * k); x = 290 + (x - 290) * (1 - 0.08 * ex * k); }
    let q = [x, y];
    q = bulge(q, [290, 528], 150, 0.24 * ex);   // nose
    q = bulge(q, [292, 624], 140, 0.10 * ex);  // mouth
    q = bulge(q, [172, 425], 60, 0.10 * ex); q = bulge(q, [348, 418], 60, 0.10 * ex);
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
  const LAY = {}; window.NEY_READY = (async () => { if (!window.NEY_LAYERS) return; for (const k of ['shade', 'shade2', 'light', 'beard', 'hair']) { const im = new Image(); im.src = NEY_LAYERS[k]; await im.decode(); LAY[k] = im; } })();
  const layer = (ctx, k) => { if (LAY[k]) ctx.drawImage(LAY[k], NEY_LAYERS.x0, NEY_LAYERS.y0, NEY_LAYERS.w, NEY_LAYERS.h); };
  function rng(seed) { return () => (seed = (seed * 16807) % 2147483647, (seed - 1) / 2147483646); }

  function vec(ctx, key, ex, fill, stroke, lw) {
    const V = window.NEY_VEC && NEY_VEC[key]; if (!V) return false;
    ctx.beginPath(); for (const c of V) spline(ctx, c.pts.map(p => T(p, ex)), true);
    if (fill) { ctx.fillStyle = fill; ctx.fill('evenodd'); }
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.lineJoin = 'round'; ctx.stroke(); }
    return true;
  }
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
    const NECK = [[200, 700], [196, 820], [190, 1000], [398, 1000], [392, 820], [388, 700]];
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
    const VEC = !!window.NEY_VEC && !o.raster;
    if (VEC) { ctx.save(); ctx.beginPath(); spline(ctx, tp(FACE), true); ctx.clip(); vec(ctx, 'shade', ex, C.shade); ctx.globalAlpha = 0.5; vec(ctx, 'light', ex, C.light); ctx.globalAlpha = 1; ctx.restore(); }
    else if (LAY.shade) { ctx.save(); ctx.beginPath(); spline(ctx, tp(FACE), true); ctx.clip(); layer(ctx, 'shade'); ctx.globalAlpha = 0.45; layer(ctx, 'light'); ctx.globalAlpha = 1; ctx.restore(); }
    // blush (style signature: pink nose + cheeks)
    ellipse([160, 500], 40, 20, C.blush, null); ellipse([420, 495], 40, 20, C.blush, null);

    // ---------- beard (solid mass + hair flicks) ----------
    const BEARD = [[105, 500], [100, 560], [110, 622], [130, 682], [165, 732], [215, 772], [270, 796], [300, 799], [345, 791], [400, 766], [440, 726], [470, 670], [478, 600], [481, 520], [479, 500], [462, 560], [428, 590], [388, 588], [370, 578], [330, 567], [290, 563], [250, 567], [210, 579], [180, 590], [138, 568], [114, 530]];
    if (VEC) { ctx.save(); ctx.beginPath(); spline(ctx, tp(FACE), true); ctx.clip();
      vec(ctx, 'beard', ex, 'rgba(78,46,28,0.62)'); vec(ctx, 'chin', ex, 'rgba(52,30,18,0.35)');
      ctx.beginPath(); for (const c of NEY_VEC.beard) spline(ctx, c.pts.map(p => T(p, ex)), true); ctx.clip();
      { const R = rng(4); ctx.strokeStyle = 'rgba(40,22,12,.45)'; ctx.lineWidth = 2.2;      // stubble flicks
        for (let i = 0; i < 420; i++) { const x = 100 + R() * 380, y = 470 + R() * 330, q = T([x, y], ex); const d = ctx.getTransform().transformPoint(new DOMPoint(q[0], q[1]));
          ctx.beginPath(); ctx.moveTo(q[0], q[1]); ctx.lineTo(q[0] + (R() - .5) * 4, q[1] + 5 + R() * 5); ctx.stroke(); } }
      ctx.restore(); }
    else if (LAY.beard) { ctx.save(); ctx.beginPath(); spline(ctx, tp(FACE), true); ctx.clip(); layer(ctx, 'beard'); ctx.restore(); }
    else shape(BEARD, C.beard, null);
    // face contour ink (variable width feel: draw twice)
    shape(FACE.slice(2, 19), null, C.line, 6, false);

    // ---------- mouth ----------
    const open = face === 'pain' || face === 'shock' || face === 'grin';
    if (!open) {
      shape([[208, 616], [234, 604], [258, 598], [290, 603], [326, 598], [352, 604], [378, 614], [292, 620]], C.lipU, C.line, 3);
      shape([[210, 619], [292, 623], [376, 616], [360, 638], [292, 654], [228, 640]], C.lipL, C.line, 3);
      ellipse([292, 634], 30, 6, C.lipHi, null);
      line([[204, 617], [250, 619], [292, 623], [336, 619], [381, 614]], C.line, 4.5);
    } else {
      const h = face === 'pain' ? 70 + Math.sin(t * 30) * 6 : face === 'shock' ? 45 : 34;
      const w = face === 'shock' ? 55 : face === 'grin' ? 112 : 100;
      const M = face === 'pain' ? [[292 - w * 0.75, 640], [292 - w * 0.4, 600], [292, 594], [292 + w * 0.4, 600], [292 + w * 0.75, 640], [292 + w * 0.5, 612 + h], [292, 622 + h], [292 - w * 0.5, 612 + h]] : [[292 - w, 612], [292, 596], [292 + w, 612], [292 + w * 0.6, 612 + h * 0.9], [292, 612 + h], [292 - w * 0.6, 612 + h * 0.9]];
      shape(M, '#4a0c0e', C.line, 5);
      ctx.save(); ctx.beginPath(); spline(ctx, tp(M), true); ctx.clip();
      if (face !== 'pain') shape([[292 - w, 600], [292 + w, 600], [292 + w, 628], [292, 640], [292 - w, 628]], '#ffffff', null);       // big upper teeth
      else shape([[292 - w, 600], [292 + w, 600], [292 + w * 0.8, 614], [292 - w * 0.8, 614]], '#ffffff', null);
      for (let i = -3; i <= 3; i++) line([[292 + i * w / 4, 600], [292 + i * w / 4, 634]], 'rgba(0,0,0,.25)', 2);
      if (face === 'grin') { shape([[262, 598], [322, 598], [322, 646], [292, 650], [262, 646]], '#ffffff', 'rgba(60,30,20,.55)', 2.5); line([[292, 598], [292, 650]], 'rgba(60,30,20,.6)', 3); } // two big front teeth
      if (face !== 'grin') ellipse([292, 612 + h * 0.8], w * 0.5, h * 0.3, '#d65a5f', null);
      ctx.restore();
    }

    // ---------- nose ----------
    shape([[262, 430], [262, 480], [250, 508], [232, 516], [224, 532], [236, 550], [258, 548], [276, 558], [292, 562], [308, 558], [326, 548], [348, 550], [358, 532], [350, 516], [332, 508], [322, 480], [320, 430]], C.skin, null);
    ellipse([292, 522], 30, 22, 'rgba(232,110,100,0.45)', null);
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
      ctx.beginPath(); ctx.arc(ic[0], ic[1], 17, 0, Math.PI * 2); ctx.fillStyle = C.iris; ctx.fill();
      ctx.beginPath(); ctx.arc(ic[0], ic[1], 7, 0, Math.PI * 2); ctx.fillStyle = '#120a06'; ctx.fill();
      ctx.beginPath(); ctx.arc(ic[0] - 4, ic[1] - 5, 3.5, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill();
      ctx.beginPath(); spline(ctx, tp(up.map(([x, y]) => [x, y + 7])), false); ctx.lineWidth = 16; ctx.strokeStyle = 'rgba(90,50,30,.45)'; ctx.stroke(); // lid shadow
      ctx.restore();
      line(up, C.line, 8); line(lo, C.line, 2.5);
      line(up.slice(1, 4).map(([x, y]) => [x, y - 9]), 'rgba(58,28,15,.6)', 2.5);   // crease
    };
    line([[140, 446], [172, 452], [204, 446]], 'rgba(120,64,40,.55)', 2.5); line([[318, 440], [350, 446], [384, 438]], 'rgba(120,64,40,.55)', 2.5);
    const shock = face === 'shock';
    eye([172, 428], [212, 429], [128, 425], shock ? 400 : 416, shock ? 452 : 435, o.look || [2, 0], face === 'pain' || face === 'wink');
    eye([348, 420], [310, 423], [394, 417], shock ? 392 : 408, shock ? 446 : 428, o.look || [-2, 0], face === 'pain');

    if (face === 'pain') { // fountain tears
      for (const [ex0, d] of [[160, -1], [360, 1]]) for (let i = 0; i < 9; i++) { const k = ((t * 2.5 + i / 9) % 1), q = T([ex0, 440], ex);
        ctx.beginPath(); ctx.ellipse(q[0] + d * k * 260, q[1] - k * 120 + k * k * 380, 11, 15, 0, 0, Math.PI * 2); ctx.fillStyle = '#7fd3ff'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#1f6fb0'; ctx.stroke(); } }
    // ---------- brows (thick, straight, close to the eyes) ----------
    const lift = face === 'pain' ? -22 : face === 'shock' ? -14 : face === 'angry' ? 8 : 0;
    {
    shape([[230, 392 + lift * 0.3], [225, 376 + lift], [180, 368 + lift * 0.6], [140, 374], [108, 390], [114, 398], [150, 388], [190, 384 + lift * 0.5], [228, 396 + lift * 0.3]], C.hair, C.line, 2);
    shape([[318, 382 + lift * 0.3], [328, 366 + lift], [380, 358 + lift * 0.6], [422, 362], [458, 376], [452, 386], [410, 378], [370, 375 + lift * 0.5], [328, 386 + lift * 0.3]], C.hair, C.line, 2); }

    // ---------- hair: curly mass with scalloped outline, curls and blond tips ----------
    const HAIR = [[250, 42], [310, 40], [360, 52], [405, 70], [452, 108], [490, 150], [522, 200], [546, 250], [560, 300], [560, 342], [546, 382], [522, 412], [486, 424], [470, 400], [460, 340], [450, 300], [430, 280], [400, 262], [350, 248], [300, 240], [262, 244], [240, 266], [228, 250], [190, 255], [140, 280], [115, 320], [110, 380], [98, 412], [66, 432], [44, 400], [30, 350], [30, 300], [44, 250], [70, 200], [100, 150], [150, 100], [200, 62]];
    const th = tp(HAIR);
    if (VEC) {
      vec(ctx, 'hair', ex, '#24160e', null);
      ctx.save(); ctx.beginPath(); for (const c of NEY_VEC.hair) spline(ctx, c.pts.map(p => T(p, ex)), true); ctx.clip();
      { const R = rng(17); for (let i = 0; i < 260; i++) { const x = 20 + R() * 560, y = 30 + R() * 420, q = T([x, y], ex), r = 9 + R() * 9, a0 = R() * 6.3;
          ctx.beginPath(); ctx.arc(q[0], q[1], r, a0, a0 + 3.4); ctx.lineWidth = 3; ctx.strokeStyle = R() < 0.5 ? '#5a3a24' : '#3d2617'; ctx.lineCap = 'round'; ctx.stroke(); } }
      vec(ctx, 'blond', ex, '#d9a64e', 'rgba(70,44,16,.8)', 1.6);
      ctx.restore();
      vec(ctx, 'hair', ex, null, C.line, 6);
      ctx.restore(); return;
    }
    if (LAY.hair && !o.vectorHair) { layer(ctx, 'hair'); ctx.restore(); return; }
    // base mass
    ctx.beginPath(); spline(ctx, th, true); ctx.fillStyle = C.hair; ctx.fill();
    // fine curls: many small spiral loops (dark rim + brown/blond highlight), clipped to the silhouette
    ctx.save(); ctx.beginPath(); spline(ctx, th, true); ctx.clip();
    { const R = rng(31);
      for (let i = 0; i < 420; i++) { const x = 20 + R() * 560, y = 30 + R() * 420, q = T([x, y], ex), r = 7 + R() * 7, a0 = R() * 6.3, col = R();
        ctx.beginPath(); for (let k = 0; k <= 16; k++) { const a = a0 + k / 16 * Math.PI * 2.6, rr = r * (0.45 + 0.55 * k / 16); ctx[k ? 'lineTo' : 'moveTo'](q[0] + Math.cos(a) * rr, q[1] + Math.sin(a) * rr); }
        ctx.lineWidth = 4.5; ctx.strokeStyle = '#120a06'; ctx.stroke();
        ctx.lineWidth = 2.4; ctx.strokeStyle = col < 0.3 ? C.tip : col < 0.75 ? C.hair2 : '#6a4a32'; ctx.stroke(); } }
    ctx.restore();
    // bumpy curl silhouette ink
    { const R = rng(5); ctx.beginPath(); const n = th.length; ctx.moveTo(th[0][0], th[0][1]);
      for (let i = 0; i < n; i++) { const a = th[i], b = th[(i + 1) % n], seg = Math.hypot(b[0] - a[0], b[1] - a[1]), st = Math.max(1, Math.round(seg / 16));
        for (let j = 0; j < st; j++) { const x0 = a[0] + (b[0] - a[0]) * j / st, y0 = a[1] + (b[1] - a[1]) * j / st, x1 = a[0] + (b[0] - a[0]) * (j + 1) / st, y1 = a[1] + (b[1] - a[1]) * (j + 1) / st, nx = y1 - y0, ny = -(x1 - x0), nl = Math.hypot(nx, ny) || 1, bmp = 4 + R() * 7;
          ctx.quadraticCurveTo((x0 + x1) / 2 - nx / nl * bmp, (y0 + y1) / 2 - ny / nl * bmp, x1, y1); } }
      ctx.closePath(); ctx.lineWidth = 4; ctx.strokeStyle = C.line; ctx.stroke(); }
    // outer ink around the whole hair silhouette (soft, behind clumps already drawn)
    ctx.restore();
  }
  window.drawNeymar = drawNeymar; window.NEY_T = T;
})();
