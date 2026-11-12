// Full-body rig for the hand-drawn Neymar caricature (same flat colour + brown ink style as the head).
// Grid space continues from neymar_vector.js (head occupies y < ~910). Brazil-style kit WITHOUT crest/logos.
(function () {
  const C = {
    line: '#3a1c0f', skin: '#d8946a', shade: '#b57250', shirt: '#ffd400', shirtSh: '#e2b400', green: '#109a4a',
    shorts: '#1f4fd6', shortsSh: '#173da8', sock: '#ffffff', sockSh: '#d9dde6', boot: '#ff5a1f', bootSh: '#c63d0e', sole: '#1d1d1d',
    tattoo: 'rgba(40,30,40,.7)',
  };
  const D = a => a * Math.PI / 180;
  const dir = a => [Math.sin(D(a)), Math.cos(D(a))];          // 0 = straight down, +90 = to the right
  const add = (p, a, len) => { const d = dir(a); return [p[0] + d[0] * len, p[1] + d[1] * len]; };

  function limbPath(ctx, a, b, wa, wb) {
    const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), n = [Math.cos(ang + Math.PI / 2), Math.sin(ang + Math.PI / 2)];
    ctx.beginPath();
    ctx.moveTo(a[0] + n[0] * wa / 2, a[1] + n[1] * wa / 2);
    ctx.lineTo(b[0] + n[0] * wb / 2, b[1] + n[1] * wb / 2);
    ctx.arc(b[0], b[1], wb / 2, ang + Math.PI / 2, ang - Math.PI / 2, true);
    ctx.lineTo(a[0] - n[0] * wa / 2, a[1] - n[1] * wa / 2);
    ctx.arc(a[0], a[1], wa / 2, ang - Math.PI / 2, ang + Math.PI / 2, true);
    ctx.closePath();
    return n;
  }
  function limb(ctx, a, b, wa, wb, fill, shade, lw = 5) {
    const n = limbPath(ctx, a, b, wa, wb);
    ctx.fillStyle = fill; ctx.fill();
    if (shade) { ctx.save(); ctx.clip(); ctx.translate(n[0] * wa * 0.55, n[1] * wa * 0.55); limbPath(ctx, a, b, wa, wb); ctx.fillStyle = shade; ctx.fill(); ctx.restore(); limbPath(ctx, a, b, wa, wb); }
    ctx.strokeStyle = C.line; ctx.lineWidth = lw; ctx.lineJoin = 'round'; ctx.stroke();
  }
  function poly(ctx, pts, fill, stroke = C.line, lw = 5) {
    ctx.beginPath(); pts.forEach((p, i) => ctx[i ? 'lineTo' : 'moveTo'](p[0], p[1])); ctx.closePath();
    if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.lineJoin = 'round'; ctx.stroke(); }
  }
  function smooth(ctx, pts, fill, stroke = C.line, lw = 5) { // closed Catmull-Rom
    const n = pts.length; ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < n; i++) { const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      ctx.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
    ctx.closePath(); if (fill) { ctx.fillStyle = fill; ctx.fill(); } if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.lineJoin = 'round'; ctx.stroke(); }
  }
  function strip(ctx, a, b, wa, wb, fill) { // band without round caps (cuffs, sock tops)
    const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), n = [Math.cos(ang + Math.PI / 2), Math.sin(ang + Math.PI / 2)];
    poly(ctx, [[a[0] + n[0] * wa / 2, a[1] + n[1] * wa / 2], [b[0] + n[0] * wb / 2, b[1] + n[1] * wb / 2], [b[0] - n[0] * wb / 2, b[1] - n[1] * wb / 2], [a[0] - n[0] * wa / 2, a[1] - n[1] * wa / 2]], fill, C.line, 4);
  }
  function hand(ctx, p, a, open) {
    ctx.save(); ctx.translate(p[0], p[1]); ctx.rotate(-D(a));
    if (open) { for (let i = -2; i <= 1; i++) { ctx.save(); ctx.rotate(i * 0.22); limbPath(ctx, [0, 0], [0, 62], 18, 15); ctx.fillStyle = C.skin; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 3.5; ctx.stroke(); ctx.restore(); } }
    smooth(ctx, [[-26, -6], [24, -8], [30, 22], [16, 44], [-18, 44], [-30, 20]], C.skin, C.line, 4.5);
    limbPath(ctx, [22, 4], [40, 30], 16, 13); ctx.fillStyle = C.skin; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 3.5; ctx.stroke();
    ctx.restore();
  }
  function bootShape(ctx, p, a, face) { // a: shin angle, face: +1 toe to the right
    ctx.save(); ctx.translate(p[0], p[1]); ctx.rotate(-D(a)); ctx.scale(face * 1.35, 1.35);
    smooth(ctx, [[-30, -26], [22, -26], [48, -12], [86, 2], [92, 22], [-34, 24]], C.boot, C.line, 5);
    poly(ctx, [[-36, 18], [94, 18], [92, 30], [-34, 30]], C.sole, C.line, 4);
    ctx.fillStyle = C.sole; for (let i = 0; i < 4; i++) ctx.fillRect(-22 + i * 32, 30, 10, 10);
    ctx.strokeStyle = 'rgba(255,255,255,.75)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(-10, -4); ctx.quadraticCurveTo(30, 10, 70, 4); ctx.stroke();
    ctx.restore();
  }

  const POSES = {
    hips:      { lU: -38, lF: 70, rU: 38, rF: -70, lT: -5, lS: 0, rT: 5, rS: 0, handsOpen: false },
    celebrate: { lU: -150, lF: -165, rU: 150, rF: 165, lT: -8, lS: -2, rT: 8, rS: 2, handsOpen: true },
    kick:      { lU: -75, lF: -95, rU: 55, rF: 25, lT: -4, lS: 0, rT: 75, rS: 120, handsOpen: true },
    clutch:    { lU: 40, lF: 95, rU: 60, rF: 115, lT: 5, lS: 15, rT: 115, rS: -25, handsOpen: false },
    flail:     { lU: -130, lF: -100, rU: 120, rF: 160, lT: -40, lS: -10, rT: 50, rS: 90, handsOpen: true },
    run:       { lU: -28, lF: 35, rU: 32, rF: -40, lT: -25, lS: -75, rT: 40, rS: -5, handsOpen: false },
  };

  function drawPlayer(ctx, o = {}) {
    const p = Object.assign({}, POSES[o.pose || 'hips'], o.angles || {});
    const Y = 45; // body offset so the shirt meets the caricature neck
    const SH = { l: [92, 965 + Y], r: [508, 965 + Y] }, HIP = { l: [215, 1660 + Y], r: [385, 1660 + Y] };
    const UA = 290, FA = 260, TH = 330, SN = 330;
    const arm = (side) => {
      const s = SH[side], e = add(s, p[side + 'U'], UA), h = add(e, p[side + 'F'], FA);
      limb(ctx, s, e, 112, 92, C.skin, C.shade);
      // tattoos on forearm
      limb(ctx, e, h, 90, 68, C.skin, C.shade);
      ctx.save(); limbPath(ctx, e, h, 90, 68); ctx.clip(); ctx.strokeStyle = C.tattoo; ctx.lineWidth = 3;
      for (let i = 0; i < 3; i++) { const k0 = 0.2 + i * 0.22, q0 = [e[0] + (h[0] - e[0]) * k0, e[1] + (h[1] - e[1]) * k0], q1 = [e[0] + (h[0] - e[0]) * (k0 + 0.15), e[1] + (h[1] - e[1]) * (k0 + 0.15)]; ctx.beginPath(); ctx.moveTo(q0[0] - 20, q0[1]); ctx.bezierCurveTo(q0[0] + 25, q0[1] - 18, q1[0] - 25, q1[1] + 18, q1[0] + 20, q1[1]); ctx.stroke(); }
      ctx.restore();
      const slv = add(s, p[side + 'U'], UA * 0.5);
      limb(ctx, add(s, p[side + 'U'], -10), slv, 132, 118, C.shirt, C.shirtSh);
      strip(ctx, add(s, p[side + 'U'], UA * 0.44), add(s, p[side + 'U'], UA * 0.53), 122, 120, C.green);
      hand(ctx, h, p[side + 'F'], p.handsOpen);
    };
    const leg = (side, face) => {
      const hp = HIP[side], k = add(hp, p[side + 'T'], TH), a = add(k, p[side + 'S'], SN);
      limb(ctx, hp, k, 132, 104, C.skin, C.shade);
      const sockTop = [k[0] + (a[0] - k[0]) * 0.08, k[1] + (a[1] - k[1]) * 0.08];
      limb(ctx, sockTop, a, 106, 80, C.sock, C.sockSh);
      strip(ctx, sockTop, [k[0] + (a[0] - k[0]) * 0.2, k[1] + (a[1] - k[1]) * 0.2], 110, 106, C.sock);
      strip(ctx, [k[0] + (a[0] - k[0]) * 0.13, k[1] + (a[1] - k[1]) * 0.13], [k[0] + (a[0] - k[0]) * 0.17, k[1] + (a[1] - k[1]) * 0.17], 108, 107, C.green);
      bootShape(ctx, a, p[side + 'S'], face);
    };
    // head first: shirt collar overlaps the neck
    ctx.save();
    if (o.rot) { ctx.translate(300, 1300); ctx.rotate(o.rot); ctx.translate(-300, -1300); }
    if (o.headTilt) { ctx.translate(300, 880); ctx.rotate(o.headTilt); ctx.translate(-300, -880); }
    if (o.style === 'hamid' && window.drawNeymarH) { ctx.translate(300, 960); ctx.scale(1.3, 1.3); ctx.translate(-300, -930); drawNeymarH(ctx, { face: o.face, t: o.t, look: o.look }); }
    else drawNeymar(ctx, { ex: o.ex ?? 1.1, face: o.face, t: o.t, look: o.look });
    ctx.restore();
    ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    if (o.rot) { ctx.translate(300, 1300); ctx.rotate(o.rot); ctx.translate(-300, -1300); }
    leg('l', -1); leg('r', 1);
    // shorts
    smooth(ctx, [[128, 1480], [472, 1480], [500, 1600], [505, 1760], [330, 1772], [300, 1690], [270, 1772], [95, 1760], [100, 1600]], C.shorts, C.line, 5);
    poly(ctx, [[300, 1690], [330, 1772], [505, 1760], [500, 1700]], C.shortsSh, null);
    poly(ctx, [[460, 1500], [496, 1620], [500, 1700], [470, 1690]], C.shortsSh, null);
    // shirt
    const SHIRT = [[192, 875], [300, 915], [400, 875], [478, 900], [540, 950], [552, 1040], [512, 1130], [498, 1320], [486, 1520], [114, 1520], [102, 1320], [88, 1130], [48, 1040], [60, 950], [122, 900]];
    smooth(ctx, SHIRT, C.shirt, C.line, 5.5);
    ctx.save(); smooth(ctx, SHIRT, null, null); ctx.clip();
    smooth(ctx, [[400, 900], [560, 950], [560, 1550], [420, 1550], [450, 1300], [470, 1100]], C.shirtSh, null);
    ctx.strokeStyle = 'rgba(150,110,0,.6)'; ctx.lineWidth = 4;
    [[[170, 1250], [230, 1330]], [[380, 1180], [430, 1260]], [[260, 1420], [330, 1470]]].forEach(([a, b]) => { ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.quadraticCurveTo((a[0] + b[0]) / 2 + 20, (a[1] + b[1]) / 2, b[0], b[1]); ctx.stroke(); });
    ctx.restore();
    smooth(ctx, [[188, 872], [240, 920], [300, 940], [360, 920], [404, 872], [414, 892], [362, 946], [300, 966], [236, 946], [180, 894]], C.green, C.line, 4);
    ctx.font = '900 92px Inter, sans-serif'; ctx.textAlign = 'center'; ctx.fillStyle = C.green; ctx.lineWidth = 5; ctx.strokeStyle = C.line;
    ctx.strokeText('10', 300, 1150); ctx.fillText('10', 300, 1150);
    arm('l'); arm('r');
    ctx.restore();
  }
  window.drawPlayer = drawPlayer; window.NEY_POSES = POSES;
})();
