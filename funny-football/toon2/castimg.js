// castimg.js — AI caricature heads on the code chibi bodies (owner, 21 Nov 2026: "chibi body + AI face", "funnier, more exaggerated faces").
// Faces: cast/<name>/caric/<expr>.png (cut by cast/cut_heads.py from extreme-caricature sheets); fallback cast/<name>/<expr>.png.
//   CASTIMG.preload(['ronaldo','messi']) → sets window.CAST_READY (range_render.js waits for it)
//   chibi.draw(ctx, C, pose, 'neutral', x, y, s, { headFn: CASTIMG.head(ctx, 'ronaldo', 'smug') })
//   CASTIMG.face(ctx, 'yamal', 'cry', x, y, height, rot)   — close-ups
(function () {
  const base = (document.currentScript && document.currentScript.src || '').replace(/castimg\.js.*$/, '') + 'cast/';
  const IM = {}, EX = ['smug', 'shock', 'angry', 'laugh', 'deadpan', 'cry', 'sad', 'angry2'];
  const MAP = { neutral: 'smug', open: 'laugh', happy: 'laugh', grin: 'laugh', joy: 'laugh', siuuu: 'laugh', dizzy: 'shock', scared: 'shock', strain: 'angry', mad: 'angry', bored: 'deadpan', flat: 'deadpan', sad: 'cry' };
  const load = (key, srcs) => new Promise(r => { const i = new Image(); let k = 0; i.onload = () => { IM[key] = i; r(); }; i.onerror = () => { if (++k < srcs.length) i.src = srcs[k]; else r(); }; i.src = srcs[0]; });
  function preload(names) { const p = Promise.all(names.flatMap(n => EX.map(e => load(n + '/' + e, [`${base}${n}/caric/${e}.png`, `${base}${n}/${e}.png`])))); window.CAST_READY = Promise.all([window.CAST_READY, p].filter(Boolean)); return p; }
  const get = (n, e) => IM[n + '/' + e] || IM[n + '/' + (MAP[e] || 'smug')] || IM[n + '/smug'];
  // head on the chibi: the image (head + neck + collar) is sized by height so every expression is the same size;
  // its collar overlaps the top of the chibi shirt. R = chibi head radius (headFn space: origin = head centre).
  function head(ctx, n, e, o = {}) {
    return (R) => { const im = get(n, typeof e === 'function' ? e() : e); if (!im) return; const h = R * (o.size || 2.35), w = h * im.width / im.height;   // trimmed at the neck: the chibi's own collar shows below
      ctx.drawImage(im, -w / 2 + (o.dx || 0) * R, R * 0.78 - h, w, h);
      if (o.collar) { // the shirt collar wraps the neck, so the head sits IN the shirt instead of on top of it
        const cy = R * 0.74, cw = R * 0.62; ctx.save(); ctx.lineCap = 'round';
        ctx.beginPath(); ctx.ellipse(0, cy, cw, R * 0.2, 0, 0.05 * Math.PI, 0.95 * Math.PI); ctx.lineWidth = R * 0.2; ctx.strokeStyle = '#111'; ctx.stroke();
        ctx.lineWidth = R * 0.13; ctx.strokeStyle = o.collar; ctx.stroke(); ctx.restore(); } };
  }
  function face(ctx, n, e, x, y, h, rot = 0) { const im = get(n, e); if (!im) return false; const w = h * im.width / im.height;
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.drawImage(im, -w / 2, -h / 2, w, h); ctx.restore(); return true; }
  window.CASTIMG = { preload, head, face, get, EX };
})();
