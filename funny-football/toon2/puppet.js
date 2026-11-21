// puppet.js — cut-out puppets built from the AI character sheets (cast/<name>/p_*.png + rig.json, made by cast/make_puppet.py).
// Same drawing for body and face, so the hero characters no longer look like an AI head glued on a code chibi.
//   PUPPET.load(['mbappe','yamal'])  → promise; sets window.CAST_READY so range_render.js waits for it
//   PUPPET.draw(ctx, 'yamal', { x, y /*feet*/, h /*px tall*/, flip, rot /*rad around feet*/, sq /*squash*/,
//       armL, armR /*deg, + = raise outward*/, legL, legR /*deg, + = outward*/, tilt /*head rad*/, expr /*smug|shock|angry|laugh|deadpan|cry*/,
//       bob /*px*/, shadow /*bool*/ })
// L / R are screen-left / screen-right of the unflipped drawing.
(function () {
  const base = (document.currentScript && document.currentScript.src || '').replace(/puppet\.js.*$/, '') + 'cast/';
  const P = {}, EX = ['smug', 'shock', 'angry', 'laugh', 'deadpan', 'cry'];
  const MAP = { neutral: 'smug', open: 'laugh', happy: 'laugh', joy: 'laugh', sad: 'cry', dizzy: 'shock', scared: 'shock', mad: 'angry', bored: 'deadpan', flat: 'deadpan' };
  const img = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = src; });
  async function one(n) {
    if (!(window.RIGS && RIGS[n])) await new Promise(r => { const s = document.createElement('script'); s.src = `${base}${n}/rig.js`; s.onload = s.onerror = r; document.head.appendChild(s); });
    const R = window.RIGS && RIGS[n]; if (!R) return;
    const parts = {}; for (const k of Object.keys(R.parts)) parts[k] = await img(`${base}${n}/p_${k}.png`);
    const busts = {}; for (const e of EX) busts[e] = await img(`${base}${n}/${e}.png`);
    P[n] = { R, parts, busts };
  }
  function load(names) { const p = Promise.all(names.map(one)); window.CAST_READY = Promise.all([window.CAST_READY, p].filter(Boolean)); return p; }
  const rad = d => d * Math.PI / 180;
  function part(ctx, pp, k, piv, ang) {
    const im = pp.parts[k]; if (!im) return; const b = pp.R.parts[k].box;
    if (!piv || !ang) { ctx.drawImage(im, b[0], b[1]); return; }
    ctx.save(); ctx.translate(piv[0], piv[1]); ctx.rotate(ang); ctx.translate(-piv[0], -piv[1]); ctx.drawImage(im, b[0], b[1]); ctx.restore();
  }
  function head(ctx, pp, o) {
    const R = pp.R, pv = R.pivot.neck, e = o.expr && (EX.includes(o.expr) ? o.expr : MAP[o.expr]);
    ctx.save(); ctx.translate(pv[0], pv[1]); ctx.rotate(o.tilt || 0); ctx.translate(-pv[0], -pv[1]);
    const bi = e && pp.busts[e], bm = e && R.busts[e];
    if (!(bi && bm)) part(ctx, pp, 'head');                             // body's own head = neutral
    if (bi && bm) { // expression bust: hair-top → mid-neck mapped onto the body's hair-top → neck pivot, clipped at mid-neck;
      // the body's collar is drawn again over it afterwards (draw()), so the kit stays the body's kit
      const s = (pv[1] - R.head.top) / (bm.neckY - bm.top) * (o.headScale || 1), dx = R.head.cx - bm.cx * s, dy = R.head.top - bm.top * s;
      ctx.save(); ctx.beginPath(); ctx.rect(dx - 50, dy - 50, bm.size[0] * s + 100, bm.neckY * s + 50 + 6); ctx.clip();
      ctx.drawImage(bi, dx, dy, bm.size[0] * s, bm.size[1] * s); ctx.restore();
    }
    ctx.restore();
  }
  function draw(ctx, n, o) {
    const pp = P[n]; if (!pp) return false; const R = pp.R, [w, h] = R.size, s = (o.h || 600) / h, pv = R.pivot;
    ctx.save(); ctx.translate(o.x, o.y + (o.bob || 0));
    if (o.shadow !== false && !o.rot) { ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.beginPath(); ctx.ellipse(0, 4, w * s * 0.42, 16 * s / 1.1, 0, 0, 7); ctx.fill(); }
    if (o.rot) ctx.rotate(o.rot);
    const sq = o.sq || 0; ctx.scale(s * (o.flip ? -1 : 1) * (1 + sq), s * (1 - sq)); ctx.translate(-w / 2, -h);
    part(ctx, pp, 'legL', pv.hipL, rad(o.legL || 0)); part(ctx, pp, 'legR', pv.hipR, -rad(o.legR || 0));
    const arms = () => { part(ctx, pp, 'armL', pv.shL, rad(o.armL || 0)); part(ctx, pp, 'armR', pv.shR, -rad(o.armR || 0)); };
    if (o.armsBack) arms();              // arms (with sleeves) turn at the shoulder top, normally drawn over the torso
    part(ctx, pp, 'torso'); if (!o.armsBack) arms();
    head(ctx, pp, o);
    if (o.expr) { const hb = R.parts.head.box; ctx.save(); ctx.beginPath(); ctx.rect(hb[0] - 10, pv.neck[1] + 2, hb[2] - hb[0] + 20, 40); ctx.clip(); part(ctx, pp, 'torso'); ctx.restore(); } // collar over the bust's neck
    ctx.restore(); return true;
  }
  // a full expression bust on its own (close-ups): x,y = face centre
  function bust(ctx, n, e, x, y, size, o = {}) {
    const pp = P[n]; if (!pp) return false; e = EX.includes(e) ? e : MAP[e] || 'smug'; const im = pp.busts[e]; if (!im) return false;
    const w = size, h = w * im.height / im.width; ctx.save(); ctx.translate(x, y); ctx.rotate(o.rot || 0); if (o.flip) ctx.scale(-1, 1);
    if (!o.kit) { ctx.drawImage(im, -w / 2, -h * 0.42, w, h); ctx.restore(); return true; }
    // o.kit: the sheet's bust has no usable shirt (white kit fading into the white background) — draw shoulders + V collar
    // in the sheet's ink style, then the face/neck clipped along the collar line
    const bm = pp.R.busts[e], k = w / im.width; ctx.translate(-w / 2, -h * 0.42); ctx.scale(k, k);
    const cx = bm.cx, hw = bm.w, nY = bm.neckY + 0.35 * (im.height - bm.neckY), vY = nY + 0.45 * (im.height - nY), B = im.height + 400;
    const edge = [[cx + 1.4 * hw, B], [cx + 1.2 * hw, nY + 0.32 * hw], [cx + 0.62 * hw, nY + 0.04 * hw], [cx + 0.26 * hw, nY], [cx, vY], [cx - 0.26 * hw, nY], [cx - 0.62 * hw, nY + 0.04 * hw], [cx - 1.2 * hw, nY + 0.32 * hw], [cx - 1.4 * hw, B]];
    const path = () => { ctx.beginPath(); ctx.moveTo(...edge[0]); for (const p of edge.slice(1)) ctx.lineTo(...p); ctx.closePath(); };
    path(); ctx.fillStyle = o.kit; ctx.fill(); ctx.lineJoin = 'round'; ctx.lineWidth = 4.5; ctx.strokeStyle = '#111'; ctx.stroke();
    if (o.stripes) { ctx.strokeStyle = o.stripes; ctx.lineWidth = 4; for (const sd of [-1, 1]) for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.moveTo(cx + sd * (0.66 + i * 0.1) * hw, nY + (0.06 + i * 0.03) * hw); ctx.lineTo(cx + sd * (1.22 + i * 0.1) * hw, nY + (0.38 + i * 0.03) * hw); ctx.stroke(); } }
    ctx.save(); ctx.beginPath(); ctx.moveTo(-500, -500); ctx.lineTo(im.width + 500, -500); ctx.lineTo(im.width + 500, edge[1][1]); for (const p of edge.slice(1, -1)) ctx.lineTo(...p); ctx.lineTo(-500, edge[7][1]); ctx.closePath(); ctx.clip();
    ctx.drawImage(im, 0, 0); ctx.restore();
    ctx.beginPath(); for (const p of edge.slice(2, 7)) ctx.lineTo(...p); ctx.lineWidth = 9; ctx.strokeStyle = o.kit; ctx.stroke(); ctx.lineWidth = 3; ctx.strokeStyle = '#111'; ctx.stroke(); // collar band
    ctx.restore(); return true;
  }
  // ---- geometry helpers (same transform as draw(); ignores sq/bob): world position of a rig point, and arm reach (IK)
  function world(n, o, px, py) { const pp = P[n]; if (!pp) return [o.x, o.y]; const [w, h] = pp.R.size, s = (o.h || 600) / h, f = o.flip ? -1 : 1;
    let x = (px - w / 2) * s * f, y = (py - h) * s; const r = o.rot || 0; return [o.x + x * Math.cos(r) - y * Math.sin(r), o.y + x * Math.sin(r) + y * Math.cos(r)]; }
  const shoulder = (n, o, side) => { const pv = P[n].R.pivot[side === 'L' ? 'shL' : 'shR']; return world(n, o, pv[0], pv[1]); };
  function armLen(n, o, side) { const R = P[n].R, b = R.parts['arm' + side].box, pv = R.pivot[side === 'L' ? 'shL' : 'shR']; return (b[3] - pv[1] - 8) * (o.h || 600) / R.size[1]; }
  // degrees for o.armL / o.armR so the hand points at (tx,ty); clamp keeps the cut-out believable
  function reach(n, o, side, tx, ty) { const [sx, sy] = shoulder(n, o, side); const phi = Math.atan2(-(tx - sx), ty - sy) - (o.rot || 0); // canvas angle from "hanging"
    const deg = phi * 180 / Math.PI * (o.flip ? -1 : 1); return side === 'L' ? deg : -deg; }
  // point on a body at fraction f of its height from the feet (the faller's upper back), for a given rotation
  function along(n, o, f) { const r = o.rot || 0, L = (o.h || 600) * f; return [o.x + Math.sin(r) * L, o.y - Math.cos(r) * L]; }
  window.PUPPET = { load, draw, bust, P, world, shoulder, armLen, reach, along };
})();
