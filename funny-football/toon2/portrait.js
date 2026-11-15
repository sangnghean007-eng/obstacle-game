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
    shape([[205, 430], [458, 420], [468, 590], [600, 625], [60, 625], [195, 590]], SH, 5); shape([[230, 480], [440, 460], [450, 540], [390, 590], [300, 598], [235, 560]], 'rgba(55,32,20,.6)', 0);
    soft(330, 560, 120, 40, 'rgba(70,40,25,.35)'); line([[255, 470], [285, 600]], 4, 'rgba(70,40,25,.35)'); line([[420, 460], [395, 600]], 4, 'rgba(70,40,25,.35)');
    // kit collar
    if (o.kit) { shape([[60, 620], [150, 560], [240, 585], [330, 630], [420, 585], [510, 560], [600, 620], [600, 700], [60, 700]], o.kit, 5); line([[240, 585], [330, 640], [420, 585]], 14, o.trim || '#046a38'); }
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
    const SK = '#e3b391', SH = '#c08562', HAIR = '#4b301f', BEARD = '#a65a2c', BD = '#7a3e1c';
    const face = [[160, 250], [158, 320], [168, 390], [195, 460], [240, 520], [295, 548], [350, 532], [400, 480], [432, 410], [442, 330], [440, 250], [420, 190], [370, 160], [295, 152], [215, 170]];
    shape([[195, 470], [425, 460], [450, 580], [560, 640], [40, 640], [170, 580]], SH, 5);
    if (o.kit) { shape([[30, 640], [150, 585], [230, 600], [300, 650], [370, 600], [450, 585], [580, 640], [580, 720], [30, 720]], o.kit, 5); line([[230, 600], [300, 660], [370, 600]], 14, o.trim || '#111'); }
    shape([[160, 270], [134, 262], [126, 320], [140, 385], [168, 392]], SK, 5); line([[146, 290], [138, 330], [150, 365]], 3, 'rgba(90,50,30,.5)');
    shape([[440, 285], [474, 280], [486, 330], [470, 392], [442, 398]], SK, 5);
    shape(face, SK, 6);
    clipTo(face, () => { shape([[470, 160], [415, 200], [425, 330], [400, 470], [470, 560]], 'rgba(160,100,70,.3)', 0); soft(232, 305, 46, 22, 'rgba(110,60,40,.3)'); soft(342, 303, 44, 22, 'rgba(110,60,40,.3)'); soft(290, 345, 10, 30, 'rgba(255,230,210,.45)'); });
    // beard: full and dense from the cheekbones down, moustache joined
    const beard = [[158, 330], [164, 410], [190, 475], [235, 535], [290, 572], [350, 552], [400, 500], [432, 430], [444, 335], [428, 352], [400, 372], [372, 398], [340, 410], [312, 404], [285, 406], [258, 404], [226, 392], [192, 360]];
    shape(beard, BEARD, 5);
    clipTo(beard, () => { for (let i = 0; i < 120; i++) { const x = 165 + (i * 53) % 275, y = 360 + (i * 37) % 200; line([[x, y], [x + 3, y + 11]], 2.5, i % 3 ? 'rgba(80,40,20,.35)' : 'rgba(230,160,110,.35)'); } soft(290, 520, 70, 40, 'rgba(70,35,15,.35)'); });
    shape([[226, 432], [252, 410], [290, 412], [326, 410], [354, 432], [340, 444], [318, 432], [290, 436], [262, 432], [240, 446]], BD, 3); // droopy moustache
    shape([[256, 440], [290, 436], [326, 440], [316, 454], [290, 458], [266, 454]], '#b56b5a', 4); // lower lip
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
  const FACES = { ronaldo, messi };
  window.portrait = { draw(c2d, name, x, y, s, o = {}) { ctx = c2d; ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.f || 1), s); ctx.translate(-330, -300); FACES[name](o); ctx.restore(); } };
})();
