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
  function line(pts, w, col = INK, smooth = true) { shape(pts, null, 0, false, smooth); ctx.lineWidth = w; ctx.strokeStyle = col; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.stroke(); }
  function soft(x, y, rx, ry, col) { ctx.save(); ctx.translate(x, y); ctx.scale(1, ry / rx); const g = ctx.createRadialGradient(0, 0, 1, 0, 0, rx); g.addColorStop(0, col); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, rx, 0, Math.PI * 2); ctx.fill(); ctx.restore(); }
  function clipTo(pts, fn) { ctx.save(); shape(pts, null, 0); ctx.clip(); fn(); ctx.restore(); }
  function taper(a, m, b, w, col) { // tapered brow / stroke: thick in the middle
    ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.quadraticCurveTo(m[0], m[1] - w, b[0], b[1]); ctx.quadraticCurveTo(m[0], m[1] + w * 0.4, a[0], a[1]); ctx.fillStyle = col; ctx.fill(); }
  function eye(c, w, h, iris, lookX = 0, lid = 0, tilt = 0) { // almond eye centred at c
    const [x, y] = c, L = [x - w / 2, y + tilt], Rr = [x + w / 2, y - tilt];
    const up = [[L[0], L[1]], [x - w * 0.15, y - h * (1 - lid)], [Rr[0], Rr[1]]], lo = [[Rr[0], Rr[1]], [x, y + h * 0.55], [L[0], L[1]]];
    ctx.save(); ctx.beginPath(); ctx.moveTo(L[0], L[1]); ctx.quadraticCurveTo(up[1][0], up[1][1], Rr[0], Rr[1]); ctx.quadraticCurveTo(lo[1][0], lo[1][1], L[0], L[1]); ctx.closePath(); ctx.fillStyle = '#f7f1ea'; ctx.fill(); ctx.clip();
    ctx.fillStyle = iris; ctx.beginPath(); ctx.arc(x + lookX * w * 0.18, y + h * 0.05, h * 0.62, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#120a06'; ctx.beginPath(); ctx.arc(x + lookX * w * 0.18, y + h * 0.05, h * 0.3, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x + lookX * w * 0.18 - h * 0.22, y - h * 0.15, h * 0.13, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(60,30,20,.25)'; ctx.fillRect(x - w, y - h * 1.2, w * 2, h * 0.55); ctx.restore();
    ctx.beginPath(); ctx.moveTo(L[0] - 4, L[1] + 2); ctx.quadraticCurveTo(up[1][0], up[1][1] - 2, Rr[0] + 3, Rr[1]); ctx.lineWidth = 6; ctx.strokeStyle = INK; ctx.lineCap = 'round'; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(L[0] + w * 0.1, y - h * (1.25 - lid)); ctx.quadraticCurveTo(x, y - h * (1.55 - lid), Rr[0] - w * 0.05, y - h * (1.05 - lid)); ctx.lineWidth = 2.5; ctx.strokeStyle = 'rgba(60,30,20,.55)'; ctx.stroke(); // crease
    ctx.beginPath(); ctx.moveTo(L[0] + w * 0.15, y + h * 0.45); ctx.quadraticCurveTo(x, y + h * 0.75, Rr[0] - w * 0.1, y + h * 0.35); ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(60,30,20,.4)'; ctx.stroke(); }

  // ---------- RONALDO (2023 reference: long narrow face, square jaw, low tight hair, high hairline, low straight brows, deep eyes, long straight nose) ----------
  function ronaldo(o) {
    const SK = o.skin || '#d9a07a', SH = '#b47852', HL = 'rgba(255,225,200,.55)', HAIR = '#17100b';
    const ex = (x, y) => [330 + (x - 330) * (y > 380 ? 1.04 : 1), y > 420 ? 420 + (y - 420) * 1.18 : y]; // caricature: stronger, longer jaw & chin
    const face = P([[192, 150], [168, 230], [168, 300], [180, 370], [196, 432], [235, 480], [285, 508], [332, 516], [385, 500], [430, 455], [458, 400], [470, 320], [470, 240], [458, 165], [415, 112], [330, 100], [245, 112]], ex);
    // neck + traps
    shape([[190, 430], [470, 420], [495, 540], [600, 610], [60, 610], [170, 540]], SH, 5);
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
      soft(222, 350, 40, 22, 'rgba(140,80,50,.22)'); soft(440, 340, 30, 22, 'rgba(140,80,50,.25)'); line([[196, 432], [235, 480], [285, 512]], 10, 'rgba(120,70,45,.25)'); line([[458, 400], [430, 458], [385, 503]], 12, 'rgba(120,70,45,.3)');
      soft(330, 470, 140, 70, 'rgba(70,50,40,.2)'); // stubble shadow
      soft(300, 150, 70, 22, 'rgba(255,225,200,.35)'); soft(345, 300, 10, 30, HL);
      soft(262, 238, 52, 24, 'rgba(110,60,40,.28)'); soft(405, 238, 48, 24, 'rgba(110,60,40,.28)'); // deep sockets
    });
    // hair: tight faded sides + short top swept up/back, hard part on the left, high hairline with temple corners
    const hairTop = [[150, 300], [146, 220], [160, 150], [190, 82], [255, 40], [330, 28], [410, 40], [462, 80], [488, 150], [487, 250], [470, 240], [462, 170], [432, 128], [400, 112], [330, 100], [262, 108], [222, 128], [195, 150], [180, 210], [170, 300]];
    shape(hairTop, 'rgba(40,30,24,.55)', 0); // fade (skin shows through)
    const top = [[178, 150], [196, 92], [255, 48], [330, 32], [410, 44], [460, 86], [478, 140], [458, 150], [430, 122], [395, 108], [330, 98], [262, 106], [222, 124], [196, 152]];
    shape(top, HAIR, 5);
    for (let i = 0; i < 9; i++) line([[250 + i * 24, 102], [262 + i * 22, 70 - Math.sin(i) * 6], [282 + i * 18, 46 + i * 2]], 2.5, 'rgba(255,255,255,.22)');
    line([[214, 128], [228, 92], [252, 58]], 3, 'rgba(255,255,255,.55)'); // part line
    // brows: thick, straight, low
    const bt = o.brow || 0;
    taper([196, 220 + bt], [252, 200 + bt], [304, 214 - bt * 0.5], 24, '#1a120c'); taper([368, 212 - bt * 0.5], [418, 198 + bt], [464, 216 + bt], 23, '#1a120c');
    // eyes
    eye([262, 247], 80, 25, '#4a2c16', o.look || 0, o.lid || 0.12, 3); eye([406, 247], 74, 24, '#4a2c16', o.look || 0, o.lid || 0.12, -3);
    // nose: long straight bridge, rounded tip, defined nostrils
    line([[318, 240], [314, 270], [312, 300]], 3, 'rgba(110,60,40,.5)');
    shape([[300, 318], [318, 300], [340, 296], [364, 304], [380, 322], [372, 338], [352, 340], [340, 344], [326, 340], [306, 336]], 'rgba(255,220,195,.35)', 0);
    line([[300, 322], [292, 334], [306, 342], [322, 338]], 4); line([[358, 338], [374, 342], [386, 332], [378, 320]], 4); soft(340, 312, 20, 12, HL);
    // nasolabial folds + mouth
    line([[300, 345], [282, 380], [286, 410]], 3, 'rgba(110,60,40,.45)'); line([[384, 345], [402, 378], [398, 405]], 3, 'rgba(110,60,40,.45)');
    const m = o.mouth || 'open';
    if (m === 'smile') { shape([[278, 392], [310, 398], [340, 396], [372, 396], [404, 386], [392, 420], [340, 436], [292, 422]], '#7a2020', 5); clipTo([[278, 392], [310, 398], [340, 396], [372, 396], [404, 386], [392, 420], [340, 436], [292, 422]], () => { ctx.fillStyle = '#fff'; ctx.fillRect(270, 388, 140, 22); line([[300, 410], [380, 408]], 2, 'rgba(0,0,0,.2)'); }); line([[272, 388], [282, 395]], 4); line([[402, 382], [410, 390]], 4); }
    else if (m === 'open') { shape([[290, 396], [318, 388], [340, 392], [362, 388], [392, 396], [380, 418], [340, 428], [302, 418]], '#6e1b1b', 5); clipTo([[290, 396], [318, 388], [340, 392], [362, 388], [392, 396], [380, 418], [340, 428], [302, 418]], () => { ctx.fillStyle = '#fff'; ctx.fillRect(285, 390, 120, 13); }); shape([[300, 420], [340, 430], [380, 420], [372, 438], [340, 446], [308, 438]], '#c97a6a', 0); }
    else { line([[292, 400], [318, 396], [340, 400], [362, 396], [390, 400]], 5); shape([[300, 404], [340, 410], [380, 404], [370, 424], [340, 430], [310, 424]], '#c47a66', 0); line([[300, 384], [322, 380], [340, 386], [358, 380], [380, 384]], 3, 'rgba(110,60,40,.5)'); }
    line([[322, 478], [332, 488], [342, 478]], 3, 'rgba(110,60,40,.45)'); // chin cleft
  }
  // ---------- MESSI (2018 reference: oval face, swept-back wavy hair, full ginger-brown beard, heavy low brows, intense eyes) ----------
  function messi(o) {
    const SK = '#e7b896', HAIR = '#4a2e1c', BEARD = '#8a5230', HL = 'rgba(255,230,210,.5)';
    const face = [[200, 170], [182, 250], [186, 330], [205, 410], [245, 470], [300, 505], [345, 510], [395, 495], [440, 450], [465, 380], [472, 290], [462, 200], [430, 140], [330, 112], [240, 135]];
    shape([[225, 440], [440, 430], [465, 560], [560, 620], [100, 620], [195, 560]], '#c99573', 5);
    if (o.kit) { shape([[60, 620], [150, 560], [240, 585], [330, 630], [420, 585], [510, 560], [600, 620], [600, 700], [60, 700]], o.kit, 5); line([[240, 585], [330, 640], [420, 585]], 14, o.trim || '#111'); }
    shape([[175, 270], [140, 265], [128, 310], [148, 360], [182, 372]], SK, 5);
    shape(face, SK, 6);
    clipTo(face, () => { shape([[520, 150], [450, 180], [455, 320], [430, 460], [520, 520]], 'rgba(160,100,70,.3)', 0); soft(300, 175, 60, 20, 'rgba(255,230,210,.3)'); soft(265, 250, 50, 26, 'rgba(110,60,40,.35)'); soft(405, 250, 46, 26, 'rgba(110,60,40,.35)'); });
    // beard: full, covers jaw + moustache
    const beard = [[186, 300], [196, 380], [225, 450], [275, 505], [340, 530], [405, 505], [450, 445], [470, 370], [472, 300], [455, 335], [420, 360], [398, 352], [372, 366], [340, 362], [308, 366], [282, 352], [258, 360], [222, 335]];
    shape(beard, BEARD, 5); clipTo(beard, () => { for (let i = 0; i < 70; i++) { const x = 190 + (i * 53) % 280, y = 330 + (i * 37) % 190; line([[x, y], [x + 4, y + 12]], 2.5, 'rgba(60,30,15,.35)'); } });
    shape([[296, 400], [340, 394], [384, 400], [372, 418], [340, 424], [308, 418]], '#c47a66', 4); // lips peeking through
    // hair: swept back, wavy, over the ears
    shape([[170, 330], [150, 240], [168, 150], [225, 85], [320, 58], [420, 72], [480, 130], [492, 220], [478, 300], [466, 230], [450, 175], [415, 140], [360, 128], [300, 132], [250, 150], [218, 190], [200, 260], [190, 330]], HAIR, 5);
    for (const s of [[[230, 150], [250, 110], [300, 85]], [[300, 132], [330, 95], [380, 80]], [[380, 132], [420, 100], [460, 120]], [[180, 280], [175, 220], [195, 170]]]) line(s, 3, 'rgba(255,255,255,.22)');
    taper([206, 228], [258, 208], [306, 222], 24, '#3b2416'); taper([366, 220], [414, 206], [460, 224], 23, '#3b2416');
    eye([264, 254], 72, 22, '#3a2416', o.look || 0, o.lid || 0.2, 2); eye([406, 254], 68, 21, '#3a2416', o.look || 0, o.lid || 0.2, -2);
    line([[322, 250], [318, 290], [316, 320]], 3, 'rgba(110,60,40,.45)'); line([[300, 335], [294, 348], [310, 354], [326, 350]], 4); line([[356, 350], [372, 354], [384, 346], [378, 334]], 4); soft(340, 330, 18, 12, HL);
  }
  const FACES = { ronaldo, messi };
  window.portrait = { draw(c2d, name, x, y, s, o = {}) { ctx = c2d; ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.f || 1), s); ctx.translate(-330, -300); FACES[name](o); ctx.restore(); } };
})();
