// portrait.js: semi-realistic caricature heads for close-ups (higher likeness than the chibi rig).
// Built from measured proportions of reference photos (landmarks only; nothing traced or copied).
// Coordinates are in a 600x620 design box; draw(ctx, name, x, y, scale, opts) centres the face at (x, y).
(function () {
  const INK = '#22140c';
  let ctx;
  const P = (pts, ex) => pts.map(([x, y]) => ex ? ex(x, y) : [x, y]);
  function shape(pts, fill, lw = 5, close = true, smooth = true) {
    ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
    if (smooth && pts.length > 2) { for (let i = 1; i < pts.length - (close ? 0 : 1); i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; ctx.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); } if (!close) ctx.lineTo(pts[pts.length - 1][0], pts[pts.length - 1][1]); }
    else for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
    if (close) ctx.closePath(); if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (lw) { ctx.lineWidth = lw; ctx.strokeStyle = INK; ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); } }
  function rr2(x, y, w, h) { ctx.beginPath(); ctx.roundRect(x, y, w, h, [2, 2, 8, 8]); ctx.fillStyle = '#fff'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke(); }
  function ell2(x, y, rx, ry, col) { ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); ctx.fillStyle = col; ctx.fill(); }
  function line(pts, w, col = INK, smooth = true) { shape(pts, null, 0, false, smooth); ctx.lineWidth = w; ctx.strokeStyle = col; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.stroke(); }
  function soft(x, y, rx, ry, col) { ctx.save(); ctx.translate(x, y); ctx.scale(1, ry / rx); const g = ctx.createRadialGradient(0, 0, 1, 0, 0, rx); g.addColorStop(0, col); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, rx, 0, Math.PI * 2); ctx.fill(); ctx.restore(); }
  function clipTo(pts, fn) { ctx.save(); shape(pts, null, 0); ctx.clip(); fn(); ctx.restore(); }
  function taper(a, m, b, w, col) { // tapered brow / stroke: thick in the middle
    ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.quadraticCurveTo(m[0], m[1] - w, b[0], b[1]); ctx.quadraticCurveTo(m[0], m[1] + w * 0.4, a[0], a[1]); ctx.fillStyle = col; ctx.fill(); }
  function brow(pts, col) { // pts: [outerTop, peakTop, innerTop, innerBot, peakBot, outerBot]
    const [a, b, c, d, e, f] = pts; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.quadraticCurveTo(b[0], b[1], c[0], c[1]); ctx.lineTo(d[0], d[1]); ctx.quadraticCurveTo(e[0], e[1], f[0], f[1]); ctx.closePath(); ctx.fillStyle = col; ctx.fill();
    ctx.save(); ctx.clip(); for (let i = 0; i < 14; i++) { const t = i / 13, x = a[0] + (c[0] - a[0]) * t, y = a[1] + (c[1] - a[1]) * t + 6; line([[x, y + 6], [x + 6, y - 6]], 2, 'rgba(255,255,255,.12)'); } ctx.restore(); }
  // expressions: brow offsets (outer/inner, per side), eye height scale, lid, pupil scale, mouth
  const EXPR = {
    neutral: { bo: 0, bi: 0, eh: 1, lid: null, pupil: 1, mouth: null },
    siuuu: { bo: -22, bi: -14, eh: 1.25, lid: 0, pupil: 0.8, mouth: 'shout' },
    shock: { bo: -34, bi: -30, eh: 1.45, lid: 0, pupil: 0.5, mouth: 'o' },
    smug: { bo: 0, bi: 6, raiseL: -30, eh: 0.85, lid: 0.45, pupil: 1, mouth: 'smirk', look: 0.6 },
    angry: { bo: -6, bi: 16, eh: 0.9, lid: 0.2, pupil: 0.8, mouth: 'grit' },
    deadpan: { bo: 4, bi: 4, eh: 0.9, lid: 0.5, pupil: 1, mouth: 'flat' },
  };
  const exprOf = o => Object.assign({}, EXPR.neutral, EXPR[o.expr] || {});
  function browE(pts, E, left) { // pts: [outerTop, peakTop, innerTop, innerBot, peakBot, outerBot]
    const r = left ? (E.raiseL || 0) : 0, d = [E.bo + r, (E.bo + E.bi) / 2 + r, E.bi + r * 0.6];
    return pts.map((p, i) => [p[0], p[1] + d[[0, 1, 2, 2, 1, 0][i]]]); }
  let PUPIL = 1;
  function eye(c, w, h, iris, lookX = 0, lid = 0, tilt = 0) { // almond eye centred at c
    const [x, y] = c, L = [x - w / 2, y + tilt], Rr = [x + w / 2, y - tilt];
    const up = [[L[0], L[1]], [x - w * 0.15, y - h * (1 - lid)], [Rr[0], Rr[1]]], lo = [[Rr[0], Rr[1]], [x, y + h * 0.55], [L[0], L[1]]];
    ctx.save(); ctx.beginPath(); ctx.moveTo(L[0], L[1]); ctx.quadraticCurveTo(up[1][0], up[1][1], Rr[0], Rr[1]); ctx.quadraticCurveTo(lo[1][0], lo[1][1], L[0], L[1]); ctx.closePath(); ctx.fillStyle = '#f7f1ea'; ctx.fill(); ctx.clip();
    ctx.fillStyle = iris; ctx.beginPath(); ctx.arc(x + lookX * w * 0.18, y + h * 0.05, h * 0.62 * Math.max(0.6, PUPIL), 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#120a06'; ctx.beginPath(); ctx.arc(x + lookX * w * 0.18, y + h * 0.05, h * 0.3 * PUPIL, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x + lookX * w * 0.18 - h * 0.22, y - h * 0.15, h * 0.13, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(60,30,20,.25)'; ctx.fillRect(x - w, y - h * 1.2, w * 2, h * 0.55); ctx.restore();
    ctx.beginPath(); ctx.moveTo(L[0] - 4, L[1] + 2); ctx.quadraticCurveTo(up[1][0], up[1][1] - 2, Rr[0] + 3, Rr[1]); ctx.lineWidth = 6; ctx.strokeStyle = INK; ctx.lineCap = 'round'; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(L[0] + w * 0.1, y - h * (1.25 - lid)); ctx.quadraticCurveTo(x, y - h * (1.55 - lid), Rr[0] - w * 0.05, y - h * (1.05 - lid)); ctx.lineWidth = 2.5; ctx.strokeStyle = 'rgba(60,30,20,.55)'; ctx.stroke(); // crease
    ctx.beginPath(); ctx.moveTo(L[0] + w * 0.15, y + h * 0.45); ctx.quadraticCurveTo(x, y + h * 0.75, Rr[0] - w * 0.1, y + h * 0.35); ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(60,30,20,.4)'; ctx.stroke(); }

  // ---------- RONALDO (2023 reference: long narrow face, square jaw, low tight hair, high hairline, low straight brows, deep eyes, long straight nose) ----------
  function ronaldo(o) {
    const E = exprOf(o); PUPIL = E.pupil;
    const SK = o.skin || '#d9a07a', SH = '#b47852', HL = 'rgba(255,225,200,.55)', HAIR = '#17100b';
    const ex = (x, y) => [330 + (x - 330) * (y > 380 ? 1.08 : 1), y > 420 ? 420 + (y - 420) * 1.3 : y]; // caricature: stronger, longer jaw & chin
    const face = P([[192, 150], [166, 230], [166, 300], [172, 370], [182, 420], [215, 468], [270, 500], [300, 512], [345, 514], [395, 496], [440, 452], [462, 400], [472, 320], [470, 240], [458, 165], [415, 112], [330, 100], [245, 112]], ex);
    // neck + traps
    if (!o.headOnly) { shape([[205, 430], [458, 420], [468, 590], [600, 625], [60, 625], [195, 590]], SH, 5); shape([[230, 480], [440, 460], [450, 540], [390, 590], [300, 598], [235, 560]], 'rgba(55,32,20,.6)', 0); }
    if (!o.headOnly) { soft(330, 560, 120, 40, 'rgba(70,40,25,.35)'); line([[255, 470], [285, 600]], 4, 'rgba(70,40,25,.35)'); line([[420, 460], [395, 600]], 4, 'rgba(70,40,25,.35)'); }
    // kit collar
    if (!o.headOnly) { if (o.kit) { shape([[60, 620], [150, 560], [240, 585], [330, 630], [420, 585], [510, 560], [600, 620], [600, 700], [60, 700]], o.kit, 5); line([[240, 585], [330, 640], [420, 585]], 14, o.trim || '#046a38'); } }
    // ears
    shape([[150, 262], [112, 255], [96, 300], [112, 352], [150, 378], [170, 360]], SK, 5); line([[135, 285], [120, 310], [138, 345]], 3, 'rgba(70,40,25,.6)');
    shape([[465, 290], [492, 288], [500, 320], [488, 360], [462, 372]], SK, 5);
    if (o.earring !== false) { ctx.fillStyle = '#eef2f7'; ctx.beginPath(); ctx.arc(128, 372, 7, 0, 7); ctx.fill(); ctx.lineWidth = 2.5; ctx.strokeStyle = INK; ctx.stroke(); }
    // face
    shape(face, SK, 6);
    clipTo(face, () => {
      // planes: temple/side shadow, cheekbone hollow, jaw shadow, stubble
      shape([[150, 120], [205, 150], [190, 260], [210, 330], [200, 430], [150, 500]], 'rgba(150,90,60,.35)', 0);
      shape([[520, 140], [455, 170], [462, 300], [440, 420], [520, 520]], 'rgba(150,90,60,.45)', 0);
      soft(222, 350, 36, 20, 'rgba(140,80,50,.12)'); soft(440, 340, 28, 20, 'rgba(140,80,50,.14)'); line([[196, 432], [235, 480], [285, 512]], 10, 'rgba(120,70,45,.25)'); line([[458, 400], [430, 458], [385, 503]], 12, 'rgba(120,70,45,.3)');
      soft(330, 470, 140, 70, 'rgba(70,50,40,.2)'); // stubble shadow
      soft(345, 300, 8, 28, HL);
      soft(262, 238, 52, 24, 'rgba(110,60,40,.28)'); soft(405, 238, 48, 24, 'rgba(110,60,40,.28)'); // deep sockets
    });
    // hair: tight faded sides + short top swept up/back, hard part on the left, high hairline with temple corners
    const hairTop = [[150, 300], [146, 220], [160, 150], [190, 82], [255, 40], [330, 28], [410, 40], [462, 80], [488, 150], [487, 250], [470, 240], [462, 170], [432, 128], [400, 112], [330, 100], [262, 108], [222, 128], [195, 150], [180, 210], [170, 300]];
    shape(hairTop, 'rgba(34,26,20,.78)', 0); // fade (short dark sides)
    const top = [[178, 150], [196, 92], [255, 48], [330, 32], [410, 44], [460, 86], [478, 140], [458, 150], [430, 122], [395, 108], [330, 98], [262, 106], [222, 124], [196, 152]];
    shape(top, HAIR, 5);
    for (let i = 0; i < 9; i++) line([[250 + i * 24, 102], [262 + i * 22, 70 - Math.sin(i) * 6], [282 + i * 18, 46 + i * 2]], 2.5, 'rgba(255,255,255,.22)');
    line([[214, 128], [228, 92], [252, 58]], 3, 'rgba(255,255,255,.55)'); // part line
    // brows: thick, straight, low
    const bt = o.brow || 0;
    brow(browE([[200, 206], [252, 186], [304, 208], [300, 224], [254, 205], [204, 220]], E, true), '#18100b'); brow(browE([[462, 204], [416, 184], [368, 208], [372, 223], [414, 202], [458, 218]], E, false), '#18100b');
    if (E.bi > 8) { line([[318, 214], [322, 232]], 3, 'rgba(90,50,30,.6)'); line([[344, 214], [340, 232]], 3, 'rgba(90,50,30,.6)'); } // frown lines
    if (E.bo < -20) for (let i = 0; i < 3; i++) line([[250, 150 + i * 14], [330, 144 + i * 14], [410, 150 + i * 14]], 3, 'rgba(110,60,40,.4)'); // forehead wrinkles
    // eyes
    const lk = o.look ?? E.look ?? 0, ld = E.lid ?? (o.lid || 0.12); eye([262, 247], 80, 25 * E.eh, '#4a2c16', lk, ld, 3); eye([406, 247], 74, 24 * E.eh, '#4a2c16', lk, ld, -3);
    // nose: long straight bridge, rounded tip, defined nostrils
    line([[318, 240], [314, 270], [312, 300]], 3, 'rgba(110,60,40,.5)');
    shape([[300, 318], [318, 300], [340, 296], [364, 304], [380, 322], [372, 338], [352, 340], [340, 344], [326, 340], [306, 336]], 'rgba(255,220,195,.35)', 0);
    shape([[312, 250], [326, 252], [322, 300], [300, 318], [296, 300]], 'rgba(120,70,45,.3)', 0); shape([[304, 330], [322, 326], [332, 340], [312, 344]], '#3a1d12', 0); shape([[352, 340], [364, 326], [382, 330], [372, 344]], '#3a1d12', 0); line([[298, 320], [290, 334], [306, 346], [326, 342]], 4); line([[356, 342], [374, 346], [390, 334], [380, 318]], 4); soft(342, 310, 14, 9, HL);
    // nasolabial folds + mouth
    line([[300, 345], [282, 380], [286, 410]], 3, 'rgba(110,60,40,.45)'); line([[384, 345], [402, 378], [398, 405]], 3, 'rgba(110,60,40,.45)');
    const m = E.mouth || o.mouth || 'open';
    if (m === 'shout') { const sh = [[262, 386], [300, 372], [340, 376], [380, 372], [420, 386], [408, 450], [372, 498], [340, 506], [306, 498], [272, 452]]; shape(sh, '#5a1414', 6); clipTo(sh, () => { ctx.fillStyle = '#fff'; ctx.fillRect(255, 370, 175, 24); ell2(340, 490, 50, 26, '#d0606a'); }); }
    else if (m === 'o') { const sh = [[306, 392], [340, 382], [374, 392], [380, 430], [366, 470], [340, 480], [314, 470], [300, 430]]; shape(sh, '#5a1414', 6); clipTo(sh, () => ell2(340, 470, 28, 14, '#d0606a')); }
    else if (m === 'smirk') { line([[290, 410], [330, 408], [372, 398], [404, 378]], 6); line([[400, 372], [410, 384]], 4); shape([[300, 414], [340, 418], [378, 406], [366, 426], [334, 432], [306, 426]], '#c47a66', 0); soft(400, 392, 16, 10, 'rgba(110,60,40,.35)'); }
    else if (m === 'grit') { const sh = [[278, 392], [340, 386], [402, 392], [396, 428], [340, 436], [284, 428]]; shape(sh, '#fff', 5); for (let i = 0; i < 6; i++) line([[292 + i * 20, 390], [292 + i * 20, 432]], 2.5); line([[280, 411], [400, 411]], 2.5); }
    else if (m === 'smile') { shape([[278, 392], [310, 398], [340, 396], [372, 396], [404, 386], [392, 420], [340, 436], [292, 422]], '#7a2020', 5); clipTo([[278, 392], [310, 398], [340, 396], [372, 396], [404, 386], [392, 420], [340, 436], [292, 422]], () => { ctx.fillStyle = '#fff'; ctx.fillRect(270, 388, 140, 22); line([[300, 410], [380, 408]], 2, 'rgba(0,0,0,.2)'); }); line([[272, 388], [282, 395]], 4); line([[402, 382], [410, 390]], 4); }
    else if (m === 'open') { shape([[282, 392], [312, 378], [340, 386], [368, 378], [398, 392], [362, 386], [340, 390], [316, 386]], '#a8584a', 4); shape([[290, 396], [318, 390], [340, 393], [362, 390], [392, 396], [380, 418], [340, 428], [302, 418]], '#6e1b1b', 5); clipTo([[290, 396], [318, 388], [340, 392], [362, 388], [392, 396], [380, 418], [340, 428], [302, 418]], () => { ctx.fillStyle = '#fff'; ctx.fillRect(285, 390, 120, 13); }); shape([[300, 420], [340, 430], [380, 420], [372, 438], [340, 446], [308, 438]], '#c97a6a', 0); }
    else { line([[292, 400], [318, 396], [340, 400], [362, 396], [390, 400]], 5); shape([[300, 404], [340, 410], [380, 404], [370, 424], [340, 430], [310, 424]], '#c47a66', 0); line([[300, 384], [322, 380], [340, 386], [358, 380], [380, 384]], 3, 'rgba(110,60,40,.5)'); }
    line([[322, 478], [332, 488], [342, 478]], 3, 'rgba(110,60,40,.45)'); // chin cleft
  }
  // ---------- MESSI (2018 reference, landmarks on the 600x620 grid: hair top 50, brows ~288, eyes 312, nose tip 382, mouth 440, beard chin 560) ----------
  function messi(o) {
    const E = exprOf(o); PUPIL = E.pupil;
    const SK = '#e3b391', SH = '#c08562', HAIR = '#4b301f', BEARD = '#8e5030', BD = '#6a361a';
    const face = [[160, 250], [158, 320], [168, 390], [195, 460], [240, 520], [295, 548], [350, 532], [400, 480], [432, 410], [442, 330], [440, 250], [420, 190], [370, 160], [295, 152], [215, 170]];
    if (!o.headOnly) { shape([[195, 470], [425, 460], [450, 580], [560, 640], [40, 640], [170, 580]], SH, 5); }
    if (!o.headOnly) { if (o.kit) { shape([[30, 640], [150, 585], [230, 600], [300, 650], [370, 600], [450, 585], [580, 640], [580, 720], [30, 720]], o.kit, 5); line([[230, 600], [300, 660], [370, 600]], 14, o.trim || '#111'); } }
    shape([[160, 270], [134, 262], [126, 320], [140, 385], [168, 392]], SK, 5); line([[146, 290], [138, 330], [150, 365]], 3, 'rgba(90,50,30,.5)');
    shape([[440, 285], [474, 280], [486, 330], [470, 392], [442, 398]], SK, 5);
    shape(face, SK, 6);
    clipTo(face, () => { shape([[470, 160], [415, 200], [425, 330], [400, 470], [470, 560]], 'rgba(160,100,70,.3)', 0); soft(232, 305, 46, 22, 'rgba(110,60,40,.3)'); soft(342, 303, 44, 22, 'rgba(110,60,40,.3)'); soft(290, 345, 10, 30, 'rgba(255,230,210,.45)'); });
    // beard v2 (user: "looks like a mask"): no ink on the cheek edge, feathered hair strokes, sideburns joined to the hair,
    // darker toward the jaw, tufted outline only along the bottom, soft moustache over the upper lip.
    // thin brown sideburns joining the hair
    shape([[158, 268], [176, 270], [180, 330], [166, 340]], HAIR, 0); shape([[428, 286], [444, 284], [444, 336], [430, 338]], HAIR, 0);
    const beard = [[160, 330], [158, 380], [168, 430], [192, 484], [236, 532], [290, 556], [350, 540], [398, 494], [428, 432], [442, 375], [444, 330], [428, 336], [418, 362], [398, 384], [370, 400], [340, 406], [312, 402], [285, 404], [258, 402], [228, 392], [204, 370], [184, 340], [176, 330]];
    const edge = [[176, 330], [184, 340], [204, 370], [228, 392], [258, 402], [285, 404], [312, 402], [340, 406], [370, 400], [398, 384], [418, 362], [428, 336]];
    shape(beard, BEARD, 0);
    clipTo(beard, () => {
      const g = ctx.createLinearGradient(0, 330, 0, 570); g.addColorStop(0, 'rgba(190,120,75,.3)'); g.addColorStop(0.55, 'rgba(110,58,30,.12)'); g.addColorStop(1, 'rgba(60,30,14,.5)'); ctx.fillStyle = g; ctx.fillRect(140, 260, 320, 320);
      for (let i = 0; i < 260; i++) { const x = 150 + (i * 53) % 300, y = 280 + (i * 37) % 290, a = ((x - 300) / 160) * 0.35; line([[x, y], [x + a * 10, y + 13]], 2.4, i % 3 ? 'rgba(75,35,15,.4)' : 'rgba(235,160,105,.4)'); }
    });
    // feathered top edge: short strands growing up/out over the skin, fading
    for (let i = 0; i < edge.length - 1; i++) for (let k = 0; k < 7; k++) { const t = k / 7, x = edge[i][0] + (edge[i + 1][0] - edge[i][0]) * t, y = edge[i][1] + (edge[i + 1][1] - edge[i][1]) * t, dx = (x - 300) * 0.04; line([[x, y + 5], [x + dx + (k % 2 ? 1.5 : -1.5), y - 5 - (k % 3) * 2]], 2.2, k % 2 ? 'rgba(142,80,48,.6)' : 'rgba(106,54,26,.45)'); }
    for (let i = 0; i < 40; i++) { const x = 190 + (i * 61) % 230, y = 330 + (i * 29) % 40 - (Math.abs(x - 300) < 60 ? 0 : 30); if (y < 360) { ctx.fillStyle = 'rgba(110,60,30,.35)'; ctx.fillRect(x, y, 2, 2); } } // stubble above the line
    // tufted bottom outline only
    const bot = [[159, 335], [158, 380], [168, 430], [192, 484], [236, 532], [290, 556], [350, 540], [398, 494], [428, 432], [442, 375], [444, 335]];
    ctx.beginPath(); ctx.moveTo(bot[0][0], bot[0][1]); for (let i = 0; i < bot.length - 1; i++) for (let k = 1; k <= 8; k++) { const t = k / 8, x = bot[i][0] + (bot[i + 1][0] - bot[i][0]) * t, y = bot[i][1] + (bot[i + 1][1] - bot[i][1]) * t, nx = (x - 300) * 0.03, ny = (y - 380) * 0.03; ctx.lineTo(x + (k % 2 ? nx * 0.9 : 0), y + (k % 2 ? ny * 0.9 : 0)); }
    ctx.lineWidth = 5; ctx.strokeStyle = INK; ctx.lineJoin = 'round'; ctx.stroke();
    soft(290, 470, 30, 18, 'rgba(60,28,10,.45)'); // soul patch shadow under the lip
    // lips + soft moustache (no outline), strands falling over the upper lip
    shape([[256, 440], [290, 436], [326, 440], [316, 454], [290, 458], [266, 454]], '#b56b5a', 3);
    shape([[224, 436], [250, 412], [290, 414], [328, 412], [356, 436], [336, 444], [290, 438], [244, 444]], BD, 0);
    for (let i = 0; i < 16; i++) { const x = 232 + i * 7.5; line([[x, 416], [x + (x - 290) * 0.08, 440 + Math.abs(x - 290) * 0.03]], 2.2, i % 2 ? 'rgba(60,28,10,.6)' : 'rgba(200,120,70,.5)'); }
    // hair: swept back, long on top, fringe falling to the left over the forehead, covers the tops of the ears
    shape([[146, 300], [140, 220], [158, 140], [205, 82], [270, 52], [345, 48], [410, 70], [452, 120], [470, 190], [470, 270], [452, 290], [440, 230], [420, 185], [380, 162], [325, 160], [282, 166], [255, 190], [228, 228], [205, 252], [180, 268], [165, 300]], HAIR, 5);
    shape([[158, 262], [168, 200], [210, 156], [266, 140], [252, 172], [224, 212], [196, 252]], HAIR, 0); line([[166, 250], [180, 205], [215, 168], [252, 150]], 3, 'rgba(255,220,180,.25)'); // fringe
    for (const s2 of [[[180, 240], [190, 170], [240, 120]], [[240, 150], [290, 95], [360, 75]], [[310, 150], [370, 100], [430, 110]], [[380, 160], [430, 150], [455, 210]], [[200, 120], [250, 80], [300, 62]]]) line(s2, 3, 'rgba(255,220,180,.25)');
    // brows: heavy, low, inner ends slightly down (the intense look)
    brow(browE([[190, 282], [236, 266], [282, 288], [280, 302], [236, 282], [194, 296]], E, true), '#3b2416'); brow(browE([[404, 278], [360, 264], [318, 288], [320, 302], [360, 280], [402, 292]], E, false), '#3b2416');
    const lk = o.look ?? E.look ?? 0, ld = E.lid ?? (o.lid || 0.25); eye([235, 313], 60, 19 * E.eh, '#3a2416', lk, ld, 2); eye([342, 312], 58, 18 * E.eh, '#3a2416', lk, ld, -2);
    if (E.mouth === 'o' || E.mouth === 'shout') { const sh = [[262, 428], [290, 420], [318, 428], [322, 462], [290, 478], [258, 462]]; shape(sh, '#4a1010', 5); }
    if (E.mouth === 'smirk') { line([[262, 446], [300, 444], [330, 432]], 5); }
    // nose: bridge, rounded tip, nostrils
    line([[288, 312], [282, 350], [276, 372]], 3, 'rgba(110,60,40,.45)');
    line([[250, 380], [242, 392], [258, 400], [274, 396]], 4); line([[300, 396], [318, 400], [330, 390], [322, 378]], 4); soft(288, 382, 18, 12, 'rgba(255,230,210,.5)');
  }
  // ---------- GENERIC ENGINE: every new player is a measured spec (landmarks on the 600x620 photo grid) ----------
  function mouthAt(M, kind, lips) { const { x, y } = M, w = (kind === 'shout' || kind === 'o') ? M.w * 0.72 : M.w, h = w * (kind === 'shout' ? 0.3 : 0.35), L = x - w / 2, Rr = x + w / 2;
    if (kind === 'shout') { const sh = [[L - 10, y - 6], [x - w * 0.2, y - h * 0.5], [x + w * 0.2, y - h * 0.5], [Rr + 10, y - 6], [Rr - 4, y + h * 1.6], [x, y + h * 2.6], [L + 4, y + h * 1.6]]; shape(sh, '#5a1414', 6); clipTo(sh, () => { ctx.fillStyle = '#fff'; ctx.fillRect(L - 20, y - h, w + 40, h * 0.9); ell2(x, y + h * 2.2, w * 0.3, h * 0.7, '#d0606a'); }); return; }
    if (kind === 'o') { const sh = [[x - w * 0.22, y - h * 0.3], [x, y - h * 0.6], [x + w * 0.22, y - h * 0.3], [x + w * 0.26, y + h * 1.2], [x, y + h * 2], [x - w * 0.26, y + h * 1.2]]; shape(sh, '#5a1414', 6); return; }
    if (kind === 'smirk') { line([[L + 10, y + 8], [x, y + 6], [Rr - 10, y - 6], [Rr + 6, y - 20]], 6); shape([[L + 20, y + 12], [x, y + 18], [Rr - 16, y + 4], [Rr - 30, y + 24], [x, y + 30], [L + 26, y + 24]], lips, 0); return; }
    if (kind === 'grit') { const sh = [[L, y - h * 0.4], [Rr, y - h * 0.4], [Rr - 6, y + h * 0.8], [L + 6, y + h * 0.8]]; shape(sh, '#fff', 5); for (let i = 1; i < 6; i++) line([[L + i * w / 6, y - h * 0.4], [L + i * w / 6, y + h * 0.8]], 2.5); line([[L, y + h * 0.2], [Rr, y + h * 0.2]], 2.5); return; }
    if (kind === 'flat') { line([[L + 8, y], [x, y + 2], [Rr - 8, y]], 5); shape([[L + 18, y + 6], [x, y + 10], [Rr - 18, y + 6], [Rr - 28, y + 22], [x, y + 28], [L + 28, y + 22]], lips, 0); return; }
    // smile (default): wide grin with teeth, shallow (the grin is a signature for many players)
    const hs = w * 0.17; const sh = [[L - 6, y - hs * 0.6], [x - w * 0.25, y - hs * 0.15], [x + w * 0.25, y - hs * 0.15], [Rr + 6, y - hs * 0.7], [Rr - 16, y + hs * 0.9], [x, y + hs * 1.25], [L + 16, y + hs * 0.9]]; shape(sh, '#6e1b1b', 5);
    clipTo(sh, () => { ctx.fillStyle = '#fff'; ctx.fillRect(L - 10, y - hs * 1.2, w + 20, hs * 1.55); for (let i = 1; i < 8; i++) line([[L + i * w / 8, y - hs * 0.4], [L + i * w / 8, y + hs * 0.3]], 1.5, 'rgba(0,0,0,.18)'); });
    shape([[L + 18, y + hs * 1.0], [x, y + hs * 1.45], [Rr - 18, y + hs * 1.0], [Rr - 30, y + hs * 1.6], [x, y + hs * 2.0], [L + 30, y + hs * 1.6]], lips, 0);
    line([[L - 14, y - hs * 1.2], [L - 6, y - hs * 0.6]], 3.5, 'rgba(110,60,40,.6)'); line([[Rr + 14, y - hs * 1.3], [Rr + 6, y - hs * 0.7]], 3.5, 'rgba(110,60,40,.6)'); }
  function _oldSmile(x, y, w, h, L, Rr) {
    const sh = [[L - 6, y - h * 0.5], [x - w * 0.25, y - h * 0.1], [x + w * 0.25, y - h * 0.1], [Rr + 6, y - h * 0.6], [Rr - 14, y + h * 0.9], [x, y + h * 1.4], [L + 14, y + h * 0.9]]; shape(sh, '#6e1b1b', 5);
    clipTo(sh, () => { ctx.fillStyle = '#fff'; ctx.fillRect(L - 10, y - h, w + 20, h * 1.15); for (let i = 1; i < 8; i++) line([[L + i * w / 8, y - h * 0.4], [L + i * w / 8, y + h * 0.15]], 1.5, 'rgba(0,0,0,.18)'); ell2(x, y + h * 1.2, w * 0.25, h * 0.35, '#d0606a'); });
    line([[L - 14, y - h * 0.8], [L - 6, y - h * 0.4]], 3.5, 'rgba(110,60,40,.6)'); line([[Rr + 14, y - h * 0.9], [Rr + 6, y - h * 0.5]], 3.5, 'rgba(110,60,40,.6)'); }
  function generic(S, o) {
    const E = exprOf(o); PUPIL = E.pupil; const HL = 'rgba(255,235,215,.45)';
    if (!o.headOnly) { shape(S.neck, S.shade, 5); if (S.underJaw) shape(S.underJaw, 'rgba(60,35,22,.45)', 0); }
    if (!o.headOnly) { if (o.kit) { shape([[30, 640], [150, 585], [230, 600], [300, 650], [370, 600], [450, 585], [580, 640], [580, 720], [30, 720]], o.kit, 5); line([[230, 600], [300, 660], [370, 600]], 14, o.trim || '#111'); } }
    if (S.hairBack) shape(S.hairBack, S.hairCol, 5);
    shape(S.earL, S.skin, 5); shape(S.earR, S.skin, 5); line(S.earLine || [[S.earL[0][0] - 12, S.earL[0][1] + 25], [S.earL[0][0] - 22, S.earL[0][1] + 50], [S.earL[0][0] - 10, S.earL[0][1] + 80]], 3, 'rgba(90,50,30,.5)');
    shape(S.face, S.skin, 6);
    clipTo(S.face, () => { shape(S.sideShade, 'rgba(160,100,70,.28)', 0); for (const [x, y, rx, ry] of S.sockets) soft(x, y, rx, ry, 'rgba(110,60,40,.26)'); for (const [x, y, rx, ry, a] of (S.blush || [])) soft(x, y, rx, ry, `rgba(230,120,100,${a})`); soft(S.nose.tip[0], S.nose.tip[1] - 30, 10, 28, HL);
      if (S.freckles) for (let i = 0; i < 26; i++) { const x = S.freckles[0] + (i * 37) % S.freckles[2], y = S.freckles[1] + (i * 23) % 40; ctx.fillStyle = 'rgba(170,90,60,.35)'; ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 7); ctx.fill(); }
      if (S.jawLines) for (const l of S.jawLines) line(l, 10, 'rgba(120,70,45,.22)'); });
    if (S.cheekLines) for (const l of S.cheekLines) line(l, 3, 'rgba(110,60,40,.4)');
    // hair (front) + strands
    shape(S.hair, S.hairCol, S.hairLw ?? 5, true, !S.hairSharp); if (S.hairShade) shape(S.hairShade, 'rgba(0,0,0,.18)', 0);
    for (const l of (S.strands || [])) line(l, 3, S.strandCol || 'rgba(255,255,255,.3)');
    if (S.hairTex) clipTo(S.hair, () => { for (let i = 0; i < 160; i++) { const x = 130 + (i * 37) % 350, y = 20 + (i * 53) % 260; ctx.strokeStyle = 'rgba(255,255,255,.08)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x, y, 4, 0, Math.PI * 1.4); ctx.stroke(); } });
    if (S.goatee) { shape(S.goatee, '#2a1a10', 0); }
    // brows / eyes / nose / mouth
    brow(browE(S.browL, E, true), S.browCol); brow(browE(S.browR, E, false), S.browCol);
    const lk = o.look ?? E.look ?? 0, ld = E.lid ?? (S.lid || 0.12);
    eye([S.eyeL[0], S.eyeL[1]], S.eyeL[2], S.eyeL[3] * E.eh, S.iris, lk, ld, 2); eye([S.eyeR[0], S.eyeR[1]], S.eyeR[2], S.eyeR[3] * E.eh, S.iris, lk, ld, -2);
    const N = S.nose; line(N.bridge, 3, 'rgba(110,60,40,.45)'); shape(N.nostrilL, '#3a1d12', 0); shape(N.nostrilR, '#3a1d12', 0); line(N.wingL, 4); line(N.wingR, 4); soft(N.tip[0], N.tip[1], 16, 10, HL);
    if (S.folds) for (const l of S.folds) line(l, 3, 'rgba(110,60,40,.4)');
    mouthAt(S.mouth, E.mouth || o.mouth || S.mouth.rest || 'smile', S.lips || '#c47a66');
    if (S.buck && (E.mouth || o.mouth || S.mouth.rest) === 'smile') { const { x, y } = S.mouth; rr2(x - 25, y - 18, 23, 28); rr2(x + 2, y - 18, 23, 28); }
    if (S.chinLine && S.chinLine.length) line(S.chinLine, 3, 'rgba(110,60,40,.4)');
  }
  // ---------- HØJLUND (Commons "Rasmus Højlund with a fan": frontal; wide cheekbones, low messy honey-blond fringe, big grin, blue-grey eyes, light brows) ----------
  const HOJ = { hairSharp: true, skin: '#f0c9ae', shade: '#d6a487', hairCol: '#d9b56a', browCol: '#a88650', iris: '#6f8fa8', lips: '#d08a7a', lid: 0.1,
    neck: [[232, 420], [418, 410], [430, 590], [560, 640], [60, 640], [222, 590]], underJaw: [[240, 445], [410, 435], [418, 480], [330, 498], [245, 480]],
    face: [[170, 200], [163, 260], [170, 330], [190, 390], [225, 430], [275, 452], [322, 462], [372, 452], [425, 425], [462, 385], [488, 320], [498, 255], [492, 200], [460, 150], [330, 128], [210, 145]],
    earL: [[168, 215], [140, 205], [128, 250], [138, 295], [168, 305]], earR: [[494, 232], [520, 230], [528, 270], [514, 315], [490, 322]],
    sideShade: [[540, 150], [480, 190], [488, 300], [450, 410], [540, 480]], sockets: [[268, 242, 46, 22], [405, 242, 46, 22]], blush: [[230, 300, 40, 20, .25], [440, 300, 36, 18, .22]], freckles: [220, 280, 230],
    jawLines: [[[190, 390], [225, 430], [275, 455]], [[462, 385], [425, 425], [372, 452]]], cheekLines: [[[205, 300], [215, 330]], [[465, 300], [452, 330]]],
    hair: [[150, 205], [150, 152], [168, 112], [172, 78], [204, 88], [214, 52], [246, 62], [262, 26], [292, 46], [320, 14], [346, 38], [374, 12], [394, 40], [428, 24], [438, 58], [470, 48], [472, 86], [502, 90], [498, 122], [520, 142], [510, 176], [520, 212], [500, 214], [492, 192], [474, 204], [466, 178], [446, 190], [432, 170], [412, 186], [394, 176], [372, 196], [352, 172], [330, 188], [308, 174], [290, 196], [268, 178], [250, 194], [232, 180], [214, 204], [196, 186], [180, 214], [166, 244]],
    hairShade: [[190, 176], [260, 150], [330, 140], [400, 146], [480, 168], [470, 186], [400, 164], [330, 160], [260, 172]],
    strands: [[[220, 175], [228, 120], [215, 70]], [[262, 170], [268, 110], [262, 45]], [[305, 165], [315, 100], [320, 30]], [[350, 168], [360, 100], [372, 30]], [[395, 165], [405, 110], [428, 40]], [[440, 170], [455, 120], [468, 62]], [[480, 180], [495, 140], [500, 100]]], strandCol: 'rgba(255,240,190,.55)',
    browL: [[215, 215], [252, 202], [292, 212], [292, 222], [252, 212], [217, 224]], browR: [[440, 216], [404, 204], [362, 214], [362, 224], [404, 214], [438, 225]],
    eyeL: [265, 243, 64, 19], eyeR: [405, 245, 62, 19],
    nose: { bridge: [[330, 245], [328, 280], [326, 305]], tip: [335, 318], nostrilL: [[300, 326], [316, 322], [322, 334], [306, 338]], nostrilR: [[350, 334], [358, 322], [374, 326], [366, 338]], wingL: [[296, 312], [288, 326], [302, 338], [318, 336]], wingR: [[352, 336], [370, 338], [382, 326], [374, 312]] },
    folds: [[[280, 330], [252, 350], [242, 372]], [[392, 332], [416, 352], [420, 372]]], mouth: { x: 325, y: 368, w: 150, rest: 'smile' }, chinLine: [[300, 440], [322, 448], [344, 440]] };
  // ---------- PELÉ (Commons "Pele photo 1962": short tight-curl hair, wide nose, big warm smile, dark skin) ----------
  const PELE = { skin: '#6b4430', shade: '#4e2f1f', hairCol: '#1a120c', browCol: '#1a120c', iris: '#2a1a10', lips: '#8a4a3a', lid: 0.15, hairLw: 5,
    neck: [[200, 520], [410, 510], [430, 640], [560, 660], [60, 660], [180, 640]], underJaw: [[215, 540], [400, 530], [405, 580], [300, 600], [220, 580]],
    face: [[150, 230], [132, 300], [138, 400], [165, 480], [210, 540], [280, 568], [350, 548], [400, 492], [430, 400], [446, 300], [440, 220], [400, 170], [300, 160], [200, 172]],
    earL: [[148, 300], [122, 295], [118, 350], [135, 395], [152, 400]], earR: [[444, 270], [478, 262], [492, 310], [478, 360], [448, 368]],
    sideShade: [[520, 150], [440, 220], [446, 330], [400, 500], [520, 560]], sockets: [[205, 318, 46, 20], [345, 318, 46, 20]], blush: [],
    jawLines: [[[165, 480], [210, 540], [280, 568]], [[400, 492], [350, 548]]], cheekLines: [[[170, 360], [182, 400]], [[425, 360], [412, 400]]],
    hair: [[140, 290], [132, 220], [146, 150], [190, 82], [255, 34], [330, 22], [400, 40], [452, 100], [470, 175], [466, 250], [446, 228], [430, 195], [395, 178], [340, 172], [290, 168], [240, 176], [196, 192], [170, 220], [158, 262]],
    strands: [], hairTex: true,
    browL: [[160, 300], [205, 284], [252, 296], [250, 306], [205, 296], [162, 310]], browR: [[392, 296], [345, 282], [300, 294], [302, 304], [345, 294], [390, 306]],
    eyeL: [205, 322, 70, 17], eyeR: [345, 322, 70, 17],
    nose: { bridge: [[272, 330], [268, 370], [266, 395]], tip: [270, 408], nostrilL: [[226, 418], [246, 410], [256, 424], [236, 430]], nostrilR: [[288, 424], [298, 410], [318, 418], [308, 430]], wingL: [[222, 398], [210, 418], [228, 434], [252, 430]], wingR: [[290, 430], [314, 434], [332, 418], [320, 398]] },
    folds: [[[220, 440], [196, 470], [198, 495]], [[330, 440], [356, 468], [352, 495]]], mouth: { x: 272, y: 478, w: 165, rest: 'smile' }, chinLine: [[255, 548], [278, 556], [300, 548]] };
  // ---------- RONALDO NAZÁRIO "R9" (Commons "Ronaldo.jpeg", 2000s: round shaved head, prominent front teeth, small chin goatee) ----------
  const R9 = { skin: '#c48a62', shade: '#a26a45', hairCol: 'rgba(40,28,20,.28)', browCol: '#2a1a10', iris: '#3a2416', lips: '#a8625a', lid: 0.12, hairLw: 0,
    neck: [[190, 500], [380, 500], [400, 640], [560, 660], [60, 660], [170, 640]], underJaw: [[195, 520], [370, 515], [375, 560], [280, 580], [200, 560]],
    face: [[120, 200], [104, 260], [108, 340], [128, 420], [165, 488], [222, 532], [268, 542], [330, 522], [385, 470], [420, 400], [440, 300], [432, 200], [400, 100], [320, 30], [230, 20], [160, 70]],
    earL: [[110, 260], [86, 255], [80, 300], [92, 345], [112, 350]], earR: [[430, 250], [462, 240], [478, 300], [462, 360], [430, 372]],
    sideShade: [[520, 100], [420, 160], [440, 320], [385, 480], [520, 560]], sockets: [[150, 258, 40, 18], [262, 258, 44, 18]], blush: [[150, 360, 34, 16, .2], [300, 360, 34, 16, .2]],
    jawLines: [[[128, 420], [165, 492], [222, 540]], [[385, 470], [330, 530]]], cheekLines: [],
    hair: [[118, 205], [140, 110], [200, 40], [270, 18], [350, 34], [410, 92], [438, 190], [430, 215], [400, 140], [340, 80], [270, 66], [200, 84], [150, 140], [126, 210]],
    strands: [],
    browL: [[112, 236], [148, 224], [186, 236], [184, 244], [148, 234], [114, 246]], browR: [[300, 234], [262, 222], [222, 234], [224, 242], [262, 232], [298, 244]],
    eyeL: [152, 262, 56, 15], eyeR: [264, 262, 60, 15],
    nose: { bridge: [[208, 270], [204, 310], [202, 335]], tip: [208, 346], nostrilL: [[172, 354], [188, 346], [198, 358], [182, 364]], nostrilR: [[222, 358], [232, 346], [248, 354], [238, 364]], wingL: [[168, 336], [158, 352], [174, 366], [192, 364]], wingR: [[226, 366], [244, 366], [258, 352], [248, 336]] },
    folds: [[[160, 368], [142, 398], [146, 426]], [[262, 366], [282, 396], [278, 424]]], mouth: { x: 214, y: 430, w: 140, rest: 'smile' }, buck: true,
    goatee: [[198, 486], [222, 478], [246, 486], [242, 522], [222, 534], [202, 522]], chinLine: [] };
  const FACES = { ronaldo, messi, hojlund: o => generic(HOJ, o), pele: o => generic(PELE, o), r9: o => generic(R9, o) };
  window.portrait = { draw(c2d, name, x, y, s, o = {}) { ctx = c2d; ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.f || 1), s); ctx.translate(-330, -300); FACES[name](o); ctx.restore(); } };
})();
