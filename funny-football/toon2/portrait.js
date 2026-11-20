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
    if (S.beard) clipTo(S.face, () => { ctx.save(); ctx.filter = 'blur(4px)'; let bf = S.beardCol; if (S.beardGrad) { bf = ctx.createLinearGradient(0, S.beardGrad[0], 0, S.beardGrad[1]); bf.addColorStop(0, S.beardGrad[2]); bf.addColorStop(1, S.beardCol); } shape(S.beard, bf, 0); ctx.filter = 'none'; ctx.restore(); clipTo(S.beard, () => { for (let i = 0; i < 420; i++) { const x = 150 + (i * 47) % 320, y = 320 + (i * 29) % 260; ctx.fillStyle = i % 3 ? 'rgba(60,32,18,.22)' : 'rgba(200,140,90,.18)'; ctx.fillRect(x, y, 3, 6); } }); if (S.stache) { ctx.save(); ctx.filter = 'blur(1.5px)'; shape(S.stache, 'rgba(78,44,24,.92)', 0); ctx.restore(); } });
    if (S.fade) for (const f of S.fade) shape(f, S.fadeCol || 'rgba(40,26,16,.85)', 0);
    // hair (front) + strands
    shape(S.hair, S.hairCol, S.hairLw ?? 5, true, !S.hairSharp); if (S.hairShade) shape(S.hairShade, 'rgba(0,0,0,.18)', 0);
    for (const l of (S.strands || [])) line(l, 3, S.strandCol || 'rgba(255,255,255,.3)');
    if (S.twists) for (const T of S.twists) { const k = Math.floor(T.length * 0.4 / 2) * 2; const a = [], b = []; for (let i = 0; i < T.length; i += 2) (i <= k ? a : b).push([T[i], T[i + 1]]); b.unshift(a[a.length - 1]); line(a, 17, '#120c08'); line(a, 12, S.hairCol); line(b, 17, '#120c08'); line(b, 12, S.tipCol || '#e8c14a'); }
    if (S.curls) clipTo(S.hair, () => { let i = 0; const xs = S.hair.map(p => p[0]), ys = S.hair.map(p => p[1]); for (let y = Math.min(...ys) - 10; y < Math.max(...ys) + 10; y += 17) for (let x = Math.min(...xs) - 10; x < Math.max(...xs) + 10; x += 19) { i++; const jx = ((i * 37) % 11) - 5, jy = ((i * 23) % 9) - 4, r = 6 + (i % 3) * 2; ctx.strokeStyle = ((i * 7919) % 13 < 5) ? S.curls : 'rgba(255,248,215,.75)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(x + jx, y + jy, r, i * 0.7, i * 0.7 + 4.6); ctx.stroke(); } });
    if (S.hairTex) clipTo(S.hair, () => { for (let i = 0; i < 160; i++) { const x = 130 + (i * 37) % 350, y = 20 + (i * 53) % 260; ctx.strokeStyle = 'rgba(255,255,255,.08)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x, y, 4, 0, Math.PI * 1.4); ctx.stroke(); } });
    if (S.goatee) { shape(S.goatee, '#2a1a10', 0); }
    if (S.stache && !S.beard) shape(S.stache, 'rgba(30,18,10,.55)', 0);
    if (o.cascao) { shape([[200, 22], [262, 12], [300, 40], [280, 80], [236, 96], [196, 70], [186, 40]], '#1a120c', 4); for (let i = 0; i < 5; i++) line([[206 + i * 18, 34], [214 + i * 18, 78]], 2.5, 'rgba(255,255,255,.25)'); } // R9's famous 2002 'Cascão' fringe
    if (o.young) { ctx.save(); ctx.globalAlpha = 0.35; ctx.fillStyle = S.skin; ctx.beginPath(); ctx.ellipse(220, 520, 90, 40, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore(); }
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
  // ---------- HARRY KANE (Commons "Harry Kane 2023": frontal; swept-back light-brown quiff over a HIGH forehead with receding temples, short ginger-brown full beard, blue eyes that squint when he smiles) ----------
  const KANE = { skin: '#e8b592', shade: '#c98f6c', hairCol: '#7b5a3c', browCol: '#6b4a30', iris: '#6f8fae', lips: '#c8806e', lid: 0.3, beardCol: 'rgba(104,64,38,.96)',
    neck: [[220, 500], [420, 500], [430, 600], [560, 640], [60, 640], [210, 600]], underJaw: [[225, 520], [410, 510], [400, 545], [310, 560], [235, 545]],
    face: [[180, 230], [172, 300], [172, 360], [178, 420], [196, 480], [230, 524], [275, 548], [312, 554], [352, 545], [395, 514], [425, 466], [440, 400], [446, 330], [446, 260], [438, 200], [420, 160], [380, 136], [320, 128], [260, 134], [215, 156], [192, 192]],
    earL: [[176, 292], [134, 270], [118, 328], [132, 388], [172, 400]], earR: [[444, 300], [478, 290], [486, 345], [468, 396], [438, 404]],
    sideShade: [[540, 150], [440, 200], [448, 330], [425, 466], [540, 560]], sockets: [[258, 302, 42, 18], [372, 308, 42, 18]], blush: [[230, 365, 30, 14, .18], [400, 368, 28, 14, .16]],
    beardGrad: [345, 460, 'rgba(104,64,38,.3)'], beard: [[180, 348], [192, 390], [214, 418], [246, 432], [272, 420], [292, 413], [312, 411], [334, 413], [356, 420], [382, 432], [414, 418], [436, 390], [446, 354], [470, 420], [440, 520], [380, 580], [310, 600], [240, 580], [180, 520], [160, 420]],
    cheekLines: [[[212, 318], [200, 326]], [[214, 328], [204, 340]], [[420, 324], [432, 332]], [[418, 334], [428, 346]]], stache: [[258, 432], [286, 418], [312, 421], [338, 418], [366, 432], [352, 437], [312, 430], [272, 437]],
    hair: [[180, 296], [168, 250], [164, 195], [172, 145], [198, 98], [240, 60], [292, 42], [350, 46], [404, 70], [444, 110], [464, 162], [466, 230], [458, 298], [448, 302], [446, 240], [440, 196], [424, 160], [398, 146], [368, 136], [338, 132], [312, 128], [288, 130], [260, 134], [234, 146], [214, 160], [198, 196], [190, 240], [182, 292]],
    hairShade: [[200, 190], [215, 160], [260, 134], [320, 126], [380, 134], [425, 160], [440, 196], [425, 150], [380, 120], [320, 112], [260, 120], [215, 145]],
    strands: [[[222, 148], [250, 98], [298, 66]], [[268, 134], [306, 86], [362, 62]], [[322, 128], [364, 86], [416, 92]], [[376, 136], [414, 112], [452, 140]], [[196, 200], [196, 150], [222, 108]]], strandCol: 'rgba(255,225,180,.38)',
    browL: [[202, 298], [244, 280], [290, 280], [290, 292], [244, 291], [204, 308]], browR: [[332, 284], [374, 281], [416, 300], [413, 310], [374, 292], [334, 295]],
    eyeL: [258, 307, 54, 15], eyeR: [372, 313, 52, 15],
    nose: { bridge: [[312, 302], [314, 345], [316, 372]], tip: [318, 383], nostrilL: [[294, 393], [306, 387], [312, 397], [300, 401]], nostrilR: [[326, 397], [332, 387], [344, 393], [338, 401]], wingL: [[288, 376], [282, 391], [296, 403], [312, 401]], wingR: [[326, 401], [342, 403], [352, 391], [346, 376]] },
    folds: [[[276, 398], [258, 425], [256, 448]], [[360, 400], [378, 425], [378, 448]]], mouth: { x: 312, y: 448, w: 112, rest: 'smile' }, chinLine: [] };
  // ---------- LAMINE YAMAL (Commons "Lamine Yamal in 2025 (cropped)": bleached-blond curly mop on top over dark roots, dark faded sides, thick straight dark brows, young oval face, full lips) ----------
  const YAMAL = { skin: '#b98060', shade: '#96603f', hairCol: '#e6cf8f', browCol: '#1a120c', iris: '#2a1a10', lips: '#94584a', lid: 0.22, hairLw: 4, curls: 'rgba(110,80,35,.55)',
    neck: [[245, 500], [415, 500], [425, 600], [560, 640], [60, 640], [235, 600]], underJaw: [[250, 515], [410, 510], [400, 545], [330, 560], [260, 545]],
    face: [[198, 250], [190, 320], [198, 392], [220, 452], [252, 502], [292, 534], [330, 542], [368, 534], [408, 502], [440, 452], [462, 392], [468, 320], [462, 250], [448, 205], [410, 175], [330, 165], [250, 175], [212, 205]],
    earL: [[190, 300], [160, 290], [152, 340], [165, 386], [194, 394]], earR: [[470, 300], [500, 290], [508, 340], [494, 386], [466, 394]],
    fade: [[[182, 330], [184, 250], [204, 215], [222, 232], [208, 300], [196, 330]], [[478, 330], [476, 250], [456, 215], [438, 232], [452, 300], [464, 330]]],
    sideShade: [[540, 150], [462, 220], [470, 330], [414, 500], [540, 560]], sockets: [[260, 314, 42, 18], [400, 314, 42, 18]], blush: [],
    jawLines: [[[212, 452], [246, 502], [290, 532]], [[448, 452], [414, 500], [372, 530]]], cheekLines: [],
    hair: [[196, 236], [178, 206], [150, 178], [170, 160], [150, 128], [182, 112], [178, 78], [214, 72], [226, 42], [262, 52], [282, 24], [314, 42], [340, 18], [366, 40], [396, 26], [414, 56], [446, 50], [452, 84], [482, 96], [472, 128], [494, 150], [470, 172], [486, 204], [466, 236], [446, 226], [430, 246], [410, 226], [390, 248], [368, 226], [346, 246], [324, 224], [302, 248], [282, 226], [262, 244], [240, 224], [218, 242]],
    hairShade: [[196, 236], [230, 214], [300, 205], [360, 205], [430, 214], [468, 236], [430, 226], [360, 220], [300, 220], [230, 226]],
    strands: [], strandCol: 'rgba(255,255,255,.3)',
    browL: [[216, 290], [256, 279], [298, 285], [298, 299], [256, 292], [218, 302]], browR: [[444, 290], [404, 279], [362, 285], [362, 299], [404, 292], [442, 302]],
    eyeL: [260, 320, 52, 14], eyeR: [400, 320, 52, 14],
    nose: { bridge: [[330, 322], [328, 362], [326, 392]], tip: [330, 404], nostrilL: [[300, 414], [314, 406], [322, 418], [306, 422]], nostrilR: [[338, 418], [346, 406], [360, 414], [354, 422]], wingL: [[290, 392], [282, 412], [298, 426], [318, 424]], wingR: [[342, 424], [362, 426], [378, 412], [370, 392]] },
    folds: [], mouth: { x: 330, y: 466, w: 108, rest: 'smile' }, chinLine: [[310, 518], [330, 524], [350, 518]] };
  // ---------- UNAI SIMÓN (Commons "Unai Simon France v Spain 7.24.26-066": near-frontal; short textured dark hair with a high fade, thick straight low brows, long straight nose, full dark beard) ----------
  const SIMON = { skin: '#e3b08c', shade: '#c48d6a', hairCol: '#3a2a1e', browCol: '#2a1c12', iris: '#4a3020', lips: '#b9786a', lid: 0.1, hairLw: 4, hairSharp: true, hairTex: true, beardCol: 'rgba(92,60,36,.95)', beardGrad: [355, 450, 'rgba(92,60,36,.3)'],
    neck: [[235, 500], [435, 500], [445, 600], [595, 640], [75, 640], [225, 600]], underJaw: [[240, 515], [425, 510], [415, 545], [325, 560], [250, 545]],
    face: [[195, 250], [193, 320], [201, 400], [215, 460], [243, 505], [280, 528], [322, 536], [365, 528], [407, 500], [439, 452], [463, 390], [475, 320], [475, 250], [467, 200], [445, 168], [335, 150], [225, 168], [201, 200]],
    earL: [[195, 268], [169, 258], [163, 312], [175, 372], [199, 384]], earR: [[473, 270], [497, 262], [501, 318], [489, 378], [467, 390]],
    fade: [[[191, 250], [195, 190], [217, 160], [225, 200], [211, 250]], [[477, 250], [475, 190], [455, 160], [447, 200], [461, 250]]], fadeCol: 'rgba(58,42,30,.55)',
    sideShade: [[575, 150], [471, 220], [477, 330], [407, 500], [575, 560]], sockets: [[267, 282, 42, 18], [371, 282, 42, 18]], blush: [],
    beard: [[195, 350], [211, 392], [239, 410], [271, 404], [297, 398], [322, 396], [347, 398], [373, 404], [405, 410], [435, 392], [465, 350], [485, 420], [455, 520], [395, 570], [322, 590], [245, 570], [195, 520], [175, 420]],
    stache: [[273, 418], [301, 404], [322, 408], [343, 404], [371, 418], [357, 424], [322, 418], [287, 424]],
    jawLines: [], cheekLines: [], strands: [],
    hair: [[201, 205], [195, 160], [205, 118], [222, 96], [240, 72], [256, 76], [266, 56], [284, 64], [300, 48], [318, 60], [334, 46], [350, 60], [368, 52], [380, 68], [398, 64], [410, 84], [430, 86], [440, 112], [462, 120], [468, 150], [477, 168], [471, 205], [459, 176], [439, 160], [405, 152], [365, 150], [325, 150], [285, 152], [249, 160], [221, 176]],
    hairShade: [[211, 180], [249, 158], [325, 148], [405, 150], [459, 172], [435, 130], [335, 112], [235, 128]],
    browL: [[233, 246], [275, 232], [319, 234], [319, 248], [275, 245], [235, 258]], browR: [[351, 234], [393, 232], [429, 246], [427, 257], [393, 245], [351, 248]],
    eyeL: [267, 286, 56, 19], eyeR: [371, 286, 56, 19],
    nose: { bridge: [[323, 290], [322, 330], [322, 352]], tip: [325, 368], nostrilL: [[299, 378], [313, 370], [321, 382], [305, 386]], nostrilR: [[329, 382], [337, 370], [351, 378], [345, 386]], wingL: [[291, 358], [285, 376], [299, 388], [317, 386]], wingR: [[333, 386], [351, 388], [365, 376], [359, 358]] },
    folds: [], mouth: { x: 322, y: 436, w: 92, rest: 'flat' }, chinLine: [] };
  // ---------- PAU CUBARSÍ (Commons "Pau Cubarsi France v Spain 7.24.26-115": young lean face, thick messy dark-brown fringe over the forehead, faded sides, thick straight brows, long straight nose) ----------
  const CUBARSI = { skin: '#ecbf9c', shade: '#cf9b7a', hairCol: '#2e1f16', browCol: '#24170f', iris: '#5d6a48', lips: '#c57f72', lid: 0.15, hairLw: 4, 
    neck: [[210, 470], [420, 470], [430, 600], [580, 640], [60, 640], [200, 600]], underJaw: [[220, 480], [410, 475], [400, 520], [300, 540], [230, 520]],
    face: [[180, 240], [180, 310], [190, 380], [208, 436], [236, 474], [270, 496], [298, 500], [332, 490], [366, 462], [396, 420], [420, 370], [436, 310], [444, 240], [440, 196], [400, 176], [310, 168], [220, 178], [190, 200]],
    earL: [[180, 290], [156, 282], [150, 330], [162, 372], [184, 380]], earR: [[440, 292], [468, 284], [486, 330], [474, 378], [444, 388]],
    fade: [[[448, 300], [454, 240], [466, 226], [480, 270], [470, 300]]], fadeCol: 'rgba(46,31,22,.45)',
    sideShade: [[560, 150], [450, 230], [452, 330], [380, 466], [560, 540]], sockets: [[224, 266, 40, 17], [330, 270, 44, 17]], blush: [],
    jawLines: [[[202, 430], [230, 470], [268, 494]], [[412, 426], [380, 466], [340, 492]]], cheekLines: [], strands: [[[200, 200], [220, 140], [260, 90]], [[260, 205], [280, 140], [320, 70]], [[330, 200], [340, 130], [370, 60]], [[390, 205], [410, 140], [440, 80]], [[450, 215], [470, 160], [480, 110]], [[230, 120], [280, 100], [340, 90]]], strandCol: 'rgba(110,80,60,.55)',
    hair: [[176, 250], [158, 210], [150, 170], [166, 138], [158, 112], [190, 92], [210, 66], [246, 58], [272, 40], [310, 50], [340, 36], [376, 48], [406, 46], [432, 66], [470, 76], [492, 104], [496, 128], [506, 160], [508, 200], [500, 232], [488, 262], [476, 244], [468, 226], [456, 210], [438, 214], [420, 196], [400, 210], [376, 194], [352, 214], [330, 198], [306, 216], [284, 196], [262, 214], [240, 196], [216, 216], [196, 204], [186, 232]],
    hairShade: [[190, 205], [240, 190], [310, 180], [380, 186], [450, 200], [420, 160], [330, 140], [240, 150]],
    browL: [[186, 246], [222, 233], [262, 234], [262, 247], [222, 245], [188, 258]], browR: [[294, 236], [340, 234], [386, 250], [384, 262], [340, 247], [294, 249]],
    eyeL: [224, 270, 46, 15], eyeR: [330, 274, 50, 15],
    nose: { bridge: [[278, 280], [274, 320], [270, 340]], tip: [268, 350], nostrilL: [[246, 360], [258, 352], [266, 364], [252, 368]], nostrilR: [[276, 364], [284, 352], [298, 358], [292, 368]], wingL: [[238, 342], [232, 358], [246, 370], [264, 368]], wingR: [[280, 370], [298, 370], [310, 358], [302, 342]] },
    folds: [], mouth: { x: 266, y: 404, w: 74, rest: 'smile' }, chinLine: [[252, 476], [270, 482], [290, 476]] };
  // ---------- EZRI KONSA (Commons "Ezri Konsa" + "England v Panama 27 June 26-158": short black crop with a sharp line-up, long slim face, high cheekbones, small chin goatee; traits-based, no frontal photo) ----------
  const KONSA = { skin: '#6b4330', shade: '#50301f', hairCol: '#141010', browCol: '#140d08', iris: '#2a1a10', lips: '#6e3a2e', lid: 0.15, hairLw: 4, hairTex: true,
    neck: [[245, 500], [415, 500], [425, 600], [560, 640], [60, 640], [235, 600]], underJaw: [[250, 520], [410, 515], [400, 555], [330, 570], [260, 555]],
    face: [[210, 230], [204, 300], [208, 380], [222, 450], [248, 508], [286, 546], [330, 560], [374, 546], [412, 508], [438, 450], [452, 380], [456, 300], [450, 230], [440, 182], [400, 160], [330, 154], [260, 160], [220, 182]],
    earL: [[210, 290], [182, 280], [176, 334], [188, 382], [214, 390]], earR: [[450, 290], [478, 280], [484, 334], [472, 382], [446, 390]],
    sideShade: [[540, 150], [460, 220], [468, 330], [420, 500], [540, 560]], sockets: [[268, 296, 42, 18], [392, 296, 42, 18]], blush: [],
    jawLines: [[[214, 446], [240, 500], [280, 536]], [[446, 446], [420, 500], [380, 536]]], cheekLines: [[[236, 360], [250, 392]], [[424, 360], [410, 392]]], strands: [],
    hair: [[208, 250], [202, 190], [214, 140], [242, 104], [284, 82], [330, 76], [376, 82], [418, 104], [446, 140], [458, 190], [452, 250], [444, 222], [438, 192], [424, 176], [396, 166], [330, 162], [264, 166], [236, 176], [222, 192], [216, 222]],
    browL: [[230, 270], [266, 260], [304, 266], [304, 276], [266, 270], [232, 280]], browR: [[430, 270], [394, 260], [356, 266], [356, 276], [394, 270], [428, 280]],
    eyeL: [268, 300, 52, 15], eyeR: [392, 300, 52, 15],
    nose: { bridge: [[330, 300], [328, 340], [326, 366]], tip: [330, 380], nostrilL: [[296, 390], [312, 382], [322, 394], [304, 398]], nostrilR: [[338, 394], [348, 382], [364, 390], [356, 398]], wingL: [[286, 370], [278, 390], [296, 404], [318, 402]], wingR: [[342, 402], [364, 404], [382, 390], [374, 370]] },
    goatee: [[290, 506], [330, 496], [370, 506], [372, 540], [350, 566], [330, 574], [310, 566], [288, 540]],
    folds: [[[286, 410], [270, 440], [272, 462]], [[374, 410], [390, 440], [388, 462]]], mouth: { x: 330, y: 456, w: 100, rest: 'smile' }, chinLine: [] };
  // ---------- MIKEL OYARZABAL (Commons "Mikel Oyarzabal.jpg" frontal + "Argentina v Spain 19 July 2026-122" for the 2026 look: long narrow face, long nose, heavy low brows, deep-set tired eyes, short swept-up hair, stubble) ----------
  const OYAR = { skin: '#e2ad88', shade: '#c28c68', hairCol: '#2c2018', browCol: '#1e140d', iris: '#3a2416', lips: '#b9786a', lid: 0.32, hairLw: 4, hairSharp: true,
    neck: [[240, 520], [430, 520], [440, 610], [590, 640], [70, 640], [230, 610]], underJaw: [[245, 530], [425, 525], [410, 565], [330, 580], [255, 565]],
    face: [[190, 260], [188, 330], [196, 410], [212, 462], [242, 510], [286, 548], [334, 562], [382, 548], [424, 508], [452, 458], [468, 400], [472, 330], [468, 260], [450, 222], [410, 206], [330, 200], [250, 206], [208, 226]],
    earL: [[190, 330], [166, 318], [160, 368], [172, 412], [196, 420]], earR: [[470, 316], [500, 298], [514, 350], [500, 400], [470, 408]],
    sideShade: [[570, 150], [466, 240], [472, 340], [424, 508], [570, 560]], sockets: [[268, 350, 46, 22], [380, 346, 46, 22]], blush: [],
    jawLines: [[[212, 462], [242, 510], [286, 548]], [[452, 458], [424, 508], [382, 548]]], cheekLines: [],
    hair: [[196, 290], [180, 250], [180, 200], [196, 152], [220, 120], [244, 104], [266, 82], [292, 92], [316, 70], [340, 84], [366, 72], [390, 92], [418, 96], [440, 118], [462, 144], [476, 190], [478, 250], [470, 290], [464, 250], [450, 228], [426, 220], [330, 212], [240, 220], [214, 236], [202, 262]],
    hairShade: [[206, 240], [260, 226], [330, 218], [410, 224], [470, 250], [430, 190], [330, 170], [230, 190]],
    strands: [[[230, 215], [245, 150], [270, 100]], [[290, 212], [300, 150], [320, 85]], [[360, 212], [366, 150], [375, 85]], [[420, 218], [430, 160], [440, 115]]], strandCol: 'rgba(150,120,95,.5)',
    browL: [[222, 338], [264, 326], [312, 334], [310, 346], [264, 338], [224, 350]], browR: [[352, 330], [396, 320], [444, 330], [442, 342], [396, 332], [354, 342]],
    eyeL: [268, 356, 52, 15], eyeR: [380, 352, 52, 15],
    nose: { bridge: [[328, 350], [327, 405], [329, 436]], tip: [334, 450], nostrilL: [[308, 462], [322, 454], [330, 466], [314, 470]], nostrilR: [[338, 466], [346, 454], [360, 462], [354, 470]], wingL: [[294, 438], [288, 460], [304, 472], [326, 470]], wingR: [[342, 470], [364, 472], [378, 460], [372, 438]] },
    folds: [], beardCol: 'rgba(58,40,28,.5)', beardGrad: [420, 520, 'rgba(58,40,28,.12)'], beard: [[190, 400], [220, 440], [260, 462], [300, 470], [334, 468], [368, 470], [408, 462], [448, 440], [474, 400], [490, 480], [450, 560], [334, 600], [220, 560], [180, 480]], mouth: { x: 334, y: 496, w: 86, rest: 'flat' }, chinLine: [[318, 548], [334, 554], [350, 548]] };
  // ---------- NICO WILLIAMS (Commons "NICO WILLIAMS - ATHLETIC BILBAO v OSASUNA": frontal; twisted locks with bleached-blond ends sticking up and out like a crown, low dark cap, long face, full lips) ----------
  const NICO = { skin: '#55331f', shade: '#3e2414', hairCol: '#1a120c', tipCol: '#d9ad45', browCol: '#0e0906', iris: '#1e120a', lips: '#6a3428', lid: 0.22, hairLw: 4, hairTex: true,
    neck: [[245, 500], [425, 500], [435, 600], [585, 640], [65, 640], [235, 600]], underJaw: [[250, 515], [415, 510], [405, 545], [330, 560], [260, 545]],
    face: [[213, 260], [211, 330], [217, 400], [229, 446], [251, 482], [283, 510], [330, 524], [377, 510], [411, 480], [435, 440], [449, 390], [457, 330], [453, 260], [439, 226], [405, 212], [330, 208], [255, 212], [223, 230]],
    earL: [[215, 350], [187, 342], [181, 392], [193, 438], [219, 444]], earR: [[453, 340], [475, 334], [481, 380], [471, 420], [449, 428]],
    sideShade: [[565, 150], [453, 250], [457, 350], [411, 480], [565, 560]], sockets: [[263, 336, 46, 18], [380, 330, 46, 18]], blush: [],
    jawLines: [], cheekLines: [], strands: [],
    hair: [[215, 262], [211, 216], [223, 176], [251, 148], [293, 132], [330, 128], [369, 132], [411, 148], [439, 176], [453, 216], [451, 262], [441, 238], [429, 222], [395, 214], [330, 210], [265, 214], [233, 222], [221, 238]],
    twists: [[265, 150, 262, 115, 260, 80, 262, 42, 265, 5], [290, 150, 290, 120, 290, 90, 295, 72, 300, 55], [375, 140, 380, 105, 385, 70, 395, 37, 405, 5], [355, 150, 375, 130, 395, 110, 435, 100, 475, 90], [385, 160, 420, 150, 455, 140, 500, 162, 545, 185], [405, 170, 445, 180, 485, 190, 527, 217, 570, 245], [395, 175, 420, 187, 445, 200, 470, 215, 495, 230], [240, 160, 217, 140, 195, 120, 167, 85, 140, 50], [235, 175, 205, 162, 175, 150, 150, 147, 125, 145], [230, 190, 187, 192, 145, 195, 97, 200, 50, 205], [250, 190, 247, 197, 245, 205, 242, 215, 240, 225], [325, 140, 325, 115, 325, 90, 330, 72, 335, 55], [415, 160, 435, 140, 455, 120, 475, 107, 495, 95], [255, 170, 230, 175, 205, 180, 190, 190, 175, 200]],
    browL: [[235, 314], [269, 302], [305, 304], [305, 314], [269, 312], [237, 324]], browR: [[355, 304], [391, 300], [425, 312], [423, 322], [391, 310], [355, 314]],
    eyeL: [265, 340, 58, 17], eyeR: [380, 334, 58, 17],
    nose: { bridge: [[330, 340], [329, 370], [329, 386]], tip: [331, 396], nostrilL: [[295, 404], [313, 396], [325, 410], [305, 414]], nostrilR: [[337, 410], [349, 396], [367, 404], [357, 414]], wingL: [[285, 384], [275, 404], [295, 420], [323, 418]], wingR: [[339, 418], [367, 420], [387, 404], [377, 384]] },
    folds: [], mouth: { x: 331, y: 456, w: 78, rest: 'flat' }, chinLine: [[315, 506], [331, 512], [347, 506]] };
  // ---------- ELLIOT ANDERSON (Commons "England v Panama 27 June 26-075" + "England v Ghana 23 June 2026-147": pale skin, textured light-brown hair with a quiff and short sides, light brows, long slim face, deep-set eyes; traits-based, photos too small for an overlay) ----------
  const ANDERSON = { skin: '#f0c4a6', shade: '#d6a487', hairCol: '#8a5e3a', browCol: '#8a6648', iris: '#6f8fa8', lips: '#d08a7a', lid: 0.28, hairLw: 4, hairSharp: true, hairTex: true,
    neck: [[245, 500], [415, 500], [425, 600], [560, 640], [60, 640], [235, 600]], underJaw: [[250, 515], [410, 510], [400, 545], [330, 560], [260, 545]],
    face: [[206, 240], [200, 310], [206, 390], [222, 452], [250, 506], [290, 540], [330, 554], [370, 540], [410, 506], [438, 452], [454, 390], [460, 310], [454, 240], [444, 196], [404, 172], [330, 166], [256, 172], [216, 196]],
    earL: [[206, 300], [176, 290], [168, 342], [182, 392], [210, 400]], earR: [[454, 300], [484, 290], [492, 342], [478, 392], [450, 400]],
    sideShade: [[540, 150], [462, 230], [468, 330], [416, 500], [540, 560]], sockets: [[268, 300, 42, 18], [392, 300, 42, 18]], blush: [[240, 376, 30, 14, .18], [420, 376, 30, 14, .16]], freckles: [240, 350, 190],
    jawLines: [[[214, 448], [244, 500], [286, 532]], [[446, 448], [416, 500], [374, 532]]], cheekLines: [],
    hair: [[204, 260], [198, 210], [204, 166], [222, 130], [246, 100], [270, 92], [290, 70], [318, 80], [340, 62], [366, 76], [392, 72], [414, 96], [440, 112], [454, 146], [462, 190], [458, 260], [450, 228], [438, 206], [414, 194], [380, 198], [348, 186], [316, 198], [284, 190], [254, 204], [230, 206], [214, 230]],
    hairShade: [[200, 230], [240, 205], [300, 195], [380, 192], [450, 210], [430, 170], [340, 150], [240, 165]],
    strands: [[[230, 205], [270, 150], [330, 112]], [[290, 200], [330, 150], [390, 118]], [[350, 196], [390, 160], [440, 140]], [[410, 204], [440, 180], [462, 170]]], strandCol: 'rgba(230,190,140,.4)',
    browL: [[230, 268], [266, 258], [304, 264], [304, 273], [266, 267], [232, 277]], browR: [[430, 268], [394, 258], [356, 264], [356, 273], [394, 267], [428, 277]],
    eyeL: [268, 302, 50, 15], eyeR: [392, 302, 50, 15],
    nose: { bridge: [[330, 305], [329, 345], [330, 370]], tip: [334, 396], nostrilL: [[304, 404], [318, 398], [324, 408], [310, 412]], nostrilR: [[340, 408], [346, 398], [360, 404], [354, 412]], wingL: [[298, 388], [292, 404], [306, 416], [322, 414]], wingR: [[342, 416], [358, 416], [370, 404], [362, 388]] },
    folds: [], mouth: { x: 330, y: 456, w: 82, rest: 'smile' }, chinLine: [[312, 528], [330, 534], [348, 528]] };
  // ---------- DECLAN RICE (Commons "Declan Rice September 2021" frontal + "England v Ghana 23 June 2026-133" for the 2026 look: dark-brown wavy quiff with faded sides, thick straight dark brows, long straight nose, stubble beard) ----------
  const RICE = { skin: '#efc6ae', shade: '#d4a68c', hairCol: '#2c1f17', browCol: '#24170f', iris: '#5f7f94', lips: '#cc8478', lid: 0.18, hairLw: 4, beardCol: 'rgba(70,46,30,.62)', beardGrad: [390, 480, 'rgba(70,46,30,.12)'],
    neck: [[230, 520], [420, 520], [430, 610], [590, 640], [70, 640], [220, 610]], underJaw: [[235, 530], [415, 525], [400, 560], [320, 575], [245, 560]],
    face: [[192, 250], [190, 320], [198, 400], [212, 450], [238, 498], [276, 532], [320, 548], [366, 534], [406, 498], [434, 450], [458, 400], [472, 320], [472, 250], [458, 212], [420, 194], [330, 190], [240, 194], [206, 214]],
    earL: [[192, 290], [168, 280], [164, 326], [176, 362], [198, 368]], earR: [[470, 290], [492, 282], [498, 328], [486, 368], [466, 374]],
    fade: [[[188, 270], [190, 200], [208, 176], [222, 196], [208, 270]], [[474, 270], [472, 200], [454, 176], [440, 196], [456, 270]]], fadeCol: 'rgba(60,44,32,.45)',
    sideShade: [[570, 150], [470, 230], [474, 330], [406, 498], [570, 560]], sockets: [[246, 312, 44, 18], [360, 312, 44, 18]], blush: [],
    beard: [[190, 380], [212, 430], [244, 452], [276, 420], [296, 414], [320, 418], [342, 414], [364, 420], [396, 452], [430, 430], [454, 380], [480, 470], [430, 560], [320, 600], [210, 560], [170, 470]],
    stache: [[270, 424], [292, 418], [320, 421], [346, 418], [368, 424], [356, 426], [320, 423], [282, 426]],
    jawLines: [], cheekLines: [], strands: [[[220, 190], [250, 120], [310, 80]], [[280, 190], [310, 120], [360, 72]], [[350, 190], [380, 120], [420, 90]], [[420, 196], [450, 150], [460, 120]]], strandCol: 'rgba(120,90,70,.45)',
    hair: [[202, 262], [194, 210], [200, 160], [222, 116], [256, 84], [302, 62], [354, 56], [404, 66], [442, 92], [466, 134], [474, 184], [468, 262], [458, 226], [446, 206], [424, 212], [402, 200], [376, 214], [348, 202], [320, 216], [292, 204], [266, 214], [242, 202], [220, 212], [210, 230]],
    hairShade: [[210, 210], [252, 194], [330, 188], [410, 194], [458, 210], [430, 160], [330, 140], [240, 160]],
    browL: [[210, 300], [252, 287], [296, 291], [296, 302], [252, 298], [212, 310]], browR: [[332, 291], [376, 287], [418, 300], [416, 310], [376, 298], [332, 302]],
    eyeL: [248, 318, 54, 15], eyeR: [360, 318, 54, 15],
    nose: { bridge: [[302, 320], [300, 360], [298, 380]], tip: [300, 392], nostrilL: [[276, 400], [288, 394], [296, 404], [282, 408]], nostrilR: [[306, 404], [312, 394], [326, 400], [320, 408]], wingL: [[270, 384], [264, 400], [278, 412], [294, 410]], wingR: [[308, 412], [324, 412], [336, 400], [330, 384]] },
    folds: [], mouth: { x: 300, y: 446, w: 90, rest: 'flat' }, chinLine: [[302, 530], [320, 536], [338, 530]] };
  // ---------- CARICATURE MODE (Nov 16, learned from big channels): blow up the 1-2 defining traits ----------
  function xform(S, rules) { const C = JSON.parse(JSON.stringify(S)); const mp = (v, f) => Array.isArray(v) ? (typeof v[0] === 'number' && v.length >= 2 && typeof v[1] === 'number' ? f(v) : v.map(u => mp(u, f))) : (v && typeof v === 'object' ? Object.fromEntries(Object.entries(v).map(([k, u]) => [k, mp(u, f)])) : v);
    for (const [keys, fn] of rules) for (const k of keys) if (C[k] !== undefined) C[k] = mp(C[k], (p) => { const q = p.slice(); const r = fn(q[0], q[1]); q[0] = r[0]; q[1] = r[1]; if (p.length >= 4 && k.startsWith('eye')) { q[2] = p[2] * (r[2] || 1); q[3] = p[3] * (r[3] || 1); } return q; });
    if (rules.mouth) C.mouth = Object.assign({}, C.mouth, rules.mouth(C.mouth)); return C; }
  // Kane: towering forehead + tall swept quiff, long beard-chin, smaller squinting eyes
  const KANE_X = xform(KANE, [
    [['hair', 'hairShade', 'strands'], (x, y) => [330 + (x - 330) * 1.05, y < 150 ? 150 - (150 - y) * 1.8 - 55 : y - 55 * Math.max(0, Math.min(1, (300 - y) / 100))]],
    [['face'], (x, y) => [x, y < 230 ? y - 55 : y > 430 ? y + (y - 430) * 0.45 : y]],
    [['beard', 'underJaw', 'neck'], (x, y) => [x, y > 430 ? y + (y - 430) * 0.45 : y]],
    [['earL', 'earR'], (x, y) => [330 + (x - 330) * 1.12, y]],
    [['eyeL', 'eyeR'], (x, y) => [x, y, 0.85, 0.75]],
  ]); KANE_X.mouth = Object.assign({}, KANE.mouth, { y: KANE.mouth.y + 8, w: KANE.mouth.w * 1.15 });
  // Yamal: a GIANT bleached curly mop, small young face, bigger lips
  const YAMAL_X = xform(YAMAL, [
    [['hair', 'hairShade'], (x, y) => [330 + (x - 330) * 1.55, 240 - (240 - y) * 1.9]],
    [['eyeL', 'eyeR'], (x, y) => [x, y, 1.1, 1.15]],
  ]); YAMAL_X.mouth = Object.assign({}, YAMAL.mouth, { w: YAMAL.mouth.w * 1.2 });
  // ---------- RODRI (Commons "Rodri Argentina v Spain 19 July 2026-297": lifting the 2026 Golden Ball; short dark messy hair, long face, heavy-lidded deep eyes, strong nose, dark goatee over stubble) ----------
  const RODRI = { skin: '#d9a27c', shade: '#b9825e', hairCol: '#231912', browCol: '#1a120c', iris: '#3a2416', lips: '#b8705f', lid: 0.3, hairLw: 4, hairSharp: true, beardCol: 'rgba(40,28,20,.9)', beardGrad: [400, 480, 'rgba(40,28,20,.18)'],
    neck: [[250, 500], [450, 500], [460, 600], [610, 640], [90, 640], [240, 600]], underJaw: [[255, 515], [440, 510], [430, 545], [340, 560], [265, 545]],
    face: [[192, 260], [190, 320], [198, 390], [218, 448], [250, 500], [296, 530], [340, 538], [382, 512], [416, 470], [440, 414], [458, 350], [470, 280], [478, 220], [450, 180], [350, 165], [250, 172], [208, 205]],
    earL: [[196, 290], [174, 282], [170, 330], [182, 370], [200, 376]], earR: [[468, 286], [498, 278], [510, 326], [498, 368], [470, 378]],
    sideShade: [[590, 150], [478, 230], [482, 340], [428, 474], [590, 560]], sockets: [[232, 296, 44, 20], [332, 290, 44, 20]], blush: [],
    beard: [[226, 430], [250, 446], [272, 444], [294, 456], [316, 444], [342, 440], [370, 432], [402, 418], [430, 440], [410, 520], [340, 570], [264, 540], [226, 490]],
    stache: [[246, 404], [272, 394], [296, 398], [322, 394], [350, 404], [336, 410], [296, 404], [260, 410]],
    jawLines: [], cheekLines: [[[200, 320], [210, 340]], [[452, 320], [444, 340]]], strands: [],
    hair: [[192, 270], [178, 220], [182, 160], [200, 118], [226, 92], [254, 72], [282, 78], [306, 58], [334, 70], [360, 54], [386, 70], [412, 66], [438, 86], [466, 96], [488, 128], [506, 160], [512, 210], [504, 270], [490, 232], [480, 206], [454, 186], [420, 176], [380, 168], [340, 166], [300, 168], [260, 174], [230, 186], [210, 210], [202, 240]],
    hairShade: [[200, 215], [250, 180], [350, 166], [450, 186], [490, 225], [470, 150], [350, 120], [230, 140]],
    browL: [[198, 270], [236, 258], [278, 266], [278, 278], [236, 270], [200, 282]], browR: [[306, 270], [346, 258], [388, 266], [386, 278], [346, 270], [308, 282]],
    eyeL: [234, 302, 54, 15], eyeR: [334, 294, 54, 15],
    nose: { bridge: [[288, 300], [286, 340], [284, 362]], tip: [286, 376], nostrilL: [[262, 386], [276, 378], [284, 390], [268, 394]], nostrilR: [[294, 390], [302, 378], [316, 386], [310, 394]], wingL: [[254, 368], [248, 386], [262, 398], [280, 396]], wingR: [[298, 398], [316, 398], [330, 386], [322, 368]] },
    folds: [[[250, 392], [236, 420], [240, 440]], [[340, 392], [356, 418], [354, 438]]], mouth: { x: 294, y: 424, w: 92, rest: 'smile' }, chinLine: [] };
  // ---------- KYLIAN MBAPPÉ (traits only, no photo traced: shaved buzz head, round face with high wide cheekbones, big ears, arched brows, wide bright grin, thin moustache shadow) ----------
  const MBAPPE = { skin: '#8a5a3c', shade: '#6c432b', hairCol: 'rgba(25,16,10,.92)', browCol: '#1a100a', iris: '#2a1a10', lips: '#7a4434', lid: 0.08, hairLw: 0, hairTex: true,
    neck: [[245, 500], [415, 500], [425, 600], [560, 640], [60, 640], [235, 600]], underJaw: [[250, 515], [410, 510], [400, 550], [330, 562], [260, 550]],
    face: [[204, 220], [196, 300], [204, 380], [222, 448], [252, 500], [290, 532], [330, 542], [370, 532], [408, 500], [438, 448], [456, 380], [464, 300], [456, 220], [440, 166], [400, 136], [330, 126], [260, 136], [220, 166]],
    earL: [[206, 262], [150, 236], [134, 316], [154, 392], [208, 400]], earR: [[454, 262], [510, 236], [526, 316], [506, 392], [452, 400]],
    sideShade: [[540, 150], [462, 220], [470, 330], [420, 500], [540, 560]], sockets: [[268, 300, 40, 16], [392, 300, 40, 16]], blush: [],
    jawLines: [[[218, 440], [246, 494], [286, 526]], [[442, 440], [414, 494], [374, 526]]], cheekLines: [[[230, 350], [244, 384]], [[430, 350], [416, 384]]], strands: [],
    hair: [[204, 226], [206, 180], [222, 146], [256, 122], [300, 110], [330, 108], [360, 110], [404, 122], [438, 146], [454, 180], [456, 226], [448, 204], [436, 184], [410, 170], [370, 162], [330, 160], [290, 162], [250, 170], [224, 184], [212, 204]],
    browL: [[232, 268], [262, 252], [302, 258], [304, 268], [264, 262], [234, 278]], browR: [[428, 268], [398, 252], [358, 258], [356, 268], [396, 262], [426, 278]],
    eyeL: [268, 300, 50, 16], eyeR: [392, 300, 50, 16],
    nose: { bridge: [[330, 300], [328, 336], [326, 360]], tip: [330, 376], nostrilL: [[292, 388], [310, 378], [322, 392], [302, 398]], nostrilR: [[338, 392], [350, 378], [368, 388], [358, 398]], wingL: [[282, 366], [274, 388], [294, 404], [318, 402]], wingR: [[342, 402], [366, 404], [386, 388], [378, 366]] },
    stache: [[288, 420], [310, 414], [330, 416], [350, 414], [372, 420], [352, 424], [330, 421], [308, 424]],
    folds: [[[280, 404], [262, 440], [266, 466]], [[380, 404], [398, 440], [394, 466]]], mouth: { x: 330, y: 456, w: 140, rest: 'smile' }, chinLine: [] };
  // ---------- Istanbul 2005 cast (trait-based caricatures, no photo traced) ----------
  // Gerrard 2005: long face, strong long chin, very short light-brown crop, narrow eyes
  const GERRARD = Object.assign(xform(RICE, [[['face', 'underJaw', 'neck', 'jawLines'], (x, y) => [330 + (x - 330) * 0.94, y > 420 ? y + (y - 420) * 0.35 : y]], [['hair', 'hairShade', 'strands'], (x, y) => [x, y + 18]]]), { hairCol: '#8a6440', browCol: '#6b4a30', iris: '#5a7a90', beard: undefined, beardCol: undefined, beardGrad: undefined, skin: '#efc3a5', shade: '#d4a58a' });
  // Dudek: long oval face, dark short hair, heavy straight brows, big ears
  const DUDEK = Object.assign(xform(OYAR, [[['face', 'underJaw'], (x, y) => [330 + (x - 330) * 0.95, y > 420 ? y + (y - 420) * 0.25 : y]]]), { hairCol: '#2a1d14', browCol: '#1a120c', beard: undefined, beardCol: undefined, beardGrad: undefined, skin: '#ecc0a0', shade: '#cf9f80' });
  // Shevchenko: angular narrow face, short blond-brown hair, thin lips, light eyes
  const SHEVA = Object.assign(xform(HOJ, [[['face', 'underJaw', 'jawLines'], (x, y) => [330 + (x - 330) * 0.9, y > 440 ? y + (y - 440) * 0.25 : y]], [['hair', 'hairShade', 'strands'], (x, y) => [330 + (x - 330) * 0.92, y - 14]]]), { hairCol: '#b89a62', browCol: '#8a6e44', iris: '#7a9cb4', lips: '#c07a6a' });
  // Bruno Fernandes (traits only): long narrow face, big nose, thick arched brows, swept dark-brown top, light stubble, wide toothy grin
  const BRUNO = Object.assign(xform(OYAR, [[['face', 'underJaw'], (x, y) => [330 + (x - 330) * 0.93, y > 430 ? y + (y - 430) * 0.3 : y]], [['hair', 'hairShade', 'strands'], (x, y) => [x, y < 200 ? y - 25 : y]]]), { hairCol: '#3a2618', browCol: '#24170f', beardCol: 'rgba(50,32,20,.45)', beardGrad: [400, 500, 'rgba(50,32,20,.10)'] });
  BRUNO.mouth = Object.assign({}, BRUNO.mouth, { w: (BRUNO.mouth.w || 100) * 1.25 });
  // Haaland (traits only): long face + long square jaw, very light blond hair slicked back into a bun, pale skin, light brows, intense blue eyes, light stubble
  const HAALAND = Object.assign(xform(HOJ, [[['face', 'underJaw', 'jawLines', 'neck'], (x, y) => [330 + (x - 330) * 0.9, y > 300 ? y + (y - 300) * 0.6 : y]],
    [['hair', 'hairShade', 'strands'], (x, y) => [330 + (x - 330) * 0.98, y < 140 ? 140 - (140 - y) * 0.35 : y]]]), { hairCol: '#ecd9a0', browCol: '#cbb07a', iris: '#3e7fc4', skin: '#f3d3bd', shade: '#ddb398', hairSharp: false, freckles: null, beardCol: 'rgba(200,170,110,.35)', beardGrad: [380, 520, 'rgba(200,170,110,.05)'], beard: [[200, 380], [260, 460], [330, 500], [400, 460], [460, 380], [440, 470], [330, 560], [220, 470]], hairBack: [[400, 30], [391, 56], [365, 75], [330, 82], [295, 75], [269, 56], [260, 30], [269, 4], [295, -15], [330, -22], [365, -15], [391, 4]], strandCol: 'rgba(150,120,60,.45)' });
  HAALAND.hair = [[156, 215], [160, 150], [200, 104], [260, 82], [330, 76], [400, 82], [460, 104], [500, 150], [504, 215], [470, 160], [400, 128], [330, 120], [260, 128], [190, 160]]; HAALAND.strands = [[[220, 150], [280, 100], [330, 86]], [[440, 150], [380, 100], [330, 86]], [[260, 140], [300, 100], [330, 90]], [[400, 140], [360, 100], [330, 90]]]; HAALAND.hairShade = null;
  const YAMAL_D = Object.assign({}, YAMAL, { hairCol: '#1a120c' });
  // Neymar 2013 (traits only): slim oval face, narrow chin, short dark sides with a bleached-blond quiff on top, thin moustache + chin-strap beard, wide toothy grin, diamond earrings
  const NEYMAR = Object.assign(xform(YAMAL, [[['face', 'underJaw', 'jawLines', 'neck'], (x, y) => [330 + (x - 330) * 0.92, y > 420 ? y + (y - 420) * 0.25 : y]]]), { skin: '#c79068', shade: '#a8724c', hairCol: '#e8d39a', curls: null, browCol: '#2a1a10', lips: '#9a5c4a',
    hair: [[200, 236], [196, 190], [214, 150], [246, 118], [282, 96], [320, 70], [352, 58], [380, 66], [404, 86], [428, 112], [450, 150], [462, 196], [462, 236], [440, 214], [410, 196], [360, 186], [300, 186], [250, 196], [220, 214]],
    hairShade: [[214, 214], [270, 190], [330, 180], [390, 186], [446, 210], [400, 200], [330, 196], [260, 204]], strands: [[[300, 180], [320, 120], [350, 70]], [[360, 180], [370, 120], [380, 72]], [[260, 190], [270, 140], [300, 100]]], strandCol: 'rgba(150,110,40,.5)',
    fade: [[[184, 340], [186, 250], [204, 214], [230, 214], [212, 300], [198, 340]], [[476, 340], [474, 250], [456, 214], [430, 214], [448, 300], [462, 340]]], fadeCol: 'rgba(30,20,12,.9)',
    stache: [[288, 432], [310, 426], [330, 428], [350, 426], [372, 432], [352, 436], [330, 433], [308, 436]], goatee: [[312, 520], [330, 514], [348, 520], [346, 540], [330, 548], [314, 540]] });
  NEYMAR.mouth = Object.assign({}, YAMAL.mouth, { w: (YAMAL.mouth.w || 100) * 1.2 });
  // Zlatan Ibrahimović 2013 (traits only): long face, big strong nose, dark hair slicked back into a bun, thick dark brows, full dark short beard
  const ZLATAN = Object.assign(xform(SIMON, [[['face', 'underJaw', 'jawLines', 'neck', 'beard', 'stache', 'earL', 'earR', 'sideShade'], (x, y) => [330 + (x - 330) * 0.9, y > 380 ? y + (y - 380) * 0.4 : y]],
    [['nose'], (x, y) => [330 + (x - 330) * 1.5, 250 + (y - 250) * 1.45]]]), { skin: '#d9a982', shade: '#b98a64', hairCol: '#1e1510', browCol: '#140d08', iris: '#3a2416', lips: '#a8665a', hairTex: false, fade: null, beardCol: 'rgba(40,28,20,.62)', beardGrad: [400, 480, 'rgba(40,28,20,.12)'],
    hair: [[188, 250], [190, 190], [214, 146], [262, 116], [330, 106], [398, 116], [446, 146], [470, 190], [472, 250], [456, 200], [420, 168], [330, 156], [240, 168], [204, 200]],
    hairBack: [[384, 70], [376, 96], [356, 112], [330, 118], [304, 112], [284, 96], [276, 70], [284, 44], [304, 28], [330, 22], [356, 28], [376, 44]],
    strands: [[[240, 168], [270, 130], [310, 112]], [[420, 168], [390, 130], [350, 112]], [[330, 156], [330, 130], [330, 110]]], strandCol: 'rgba(90,70,55,.6)', hairShade: null });
  const ZLATAN_X = Object.assign({}, ZLATAN, { hairBack: null, strands: [[[230, 160], [200, 90], [180, 60]], [[300, 130], [290, 60], [270, 20]], [[360, 130], [380, 60], [400, 20]], [[430, 160], [470, 90], [490, 60]]], strandCol: '#1e1510' });
  const FACES = { zlatan_x: o => { FACES.zlatan(o, ZLATAN_X); }, zlatan: (o, SP = ZLATAN) => { generic(SP, o); // the trademark: a big strong nose drawn on top
    ctx.save(); const sk = '#d6a47e'; const parts = () => { ctx.beginPath(); ctx.moveTo(320, 282); ctx.quadraticCurveTo(312, 320, 308, 352); ctx.lineTo(358, 352); ctx.quadraticCurveTo(352, 320, 344, 282); ctx.closePath(); ctx.moveTo(366, 374); ctx.ellipse(334, 372, 32, 26, 0, 0, 7); ctx.moveTo(310, 384); ctx.ellipse(296, 384, 16, 13, 0, 0, 7); ctx.moveTo(388, 384); ctx.ellipse(372, 384, 16, 13, 0, 0, 7); };
    ctx.lineWidth = 9; ctx.strokeStyle = '#3a1d12'; parts(); ctx.stroke(); ctx.fillStyle = sk; parts(); ctx.fill(); ctx.fillStyle = 'rgba(160,100,70,.35)'; ctx.beginPath(); ctx.ellipse(334, 386, 26, 8, 0, 0, 7); ctx.fill();
    ctx.fillStyle = 'rgba(255,235,210,.6)'; ctx.beginPath(); ctx.ellipse(338, 360, 9, 14, 0, 0, 7); ctx.fill(); ctx.fillStyle = '#3a1d12'; for (const x of [310, 358]) { ctx.beginPath(); ctx.ellipse(x, 392, 9, 5, 0, 0, 7); ctx.fill(); } ctx.restore(); }, neymar: o => { generic(NEYMAR, o); ctx.fillStyle = '#e8f6ff'; for (const x of [166, 494]) { ctx.beginPath(); ctx.arc(x, 392, 9, 0, 7); ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#22140c'; ctx.stroke(); } }, yamal_d: o => generic(YAMAL_D, o), haaland: o => { generic(HAALAND, o); }, bruno: o => generic(BRUNO, o), gerrard: o => generic(GERRARD, o), dudek: o => generic(DUDEK, o), sheva: o => generic(SHEVA, o), mbappe: o => generic(MBAPPE, o), ronaldo, messi, hojlund: o => generic(HOJ, o), pele: o => generic(PELE, o), r9: o => generic(R9, o), kane: o => generic(KANE, o), yamal: o => generic(YAMAL, o), simon: o => generic(SIMON, o), cubarsi: o => generic(CUBARSI, o), konsa: o => generic(KONSA, o), oyarzabal: o => generic(OYAR, o), nico: o => generic(NICO, o), anderson: o => generic(ANDERSON, o), rice: o => generic(RICE, o), kane_x: o => generic(KANE_X, o), yamal_x: o => generic(YAMAL_X, o), rodri: o => generic(RODRI, o) };
  window.portrait = { draw(c2d, name, x, y, s, o = {}) { ctx = c2d; ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.f || 1), s); ctx.translate(-330, -300); FACES[name](o); ctx.restore(); } };
})();
