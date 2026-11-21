// castimg.js — AI character sheets (toon2/cast/<name>/*.png, cut by cast/cut_sheet.py) used as heads on the chibi rig.
// Likeness gate (studio/LIKENESS.md): a cast head is used whenever the sheet exists; code portraits are only the fallback.
//   CASTIMG.preload(['mbappe','yamal'])          → window.CAST_READY promise (range_render.js awaits it)
//   chibi.draw(..., { headFn: CASTIMG.head(ctx, 'mbappe', 'smug', fallbackFn) })
//   CASTIMG.face(ctx, 'yamal', 'shock', x, y, size)   — close-ups / xcu shots
//   CASTIMG.body(ctx, 'yamal', 'front', x, footY, height) — full-body turnaround (front / threequarter / side)
(function () {
  const base = (document.currentScript && document.currentScript.src || '').replace(/castimg\.js.*$/, '') + 'cast/';
  const IM = {}, EX = ['smug', 'shock', 'angry', 'laugh', 'deadpan', 'cry'], VIEWS = ['front', 'threequarter', 'side'];
  // rig / portrait expression names → the six sheet expressions
  const MAP = { neutral: 'smug', open: 'laugh', happy: 'laugh', siuuu: 'laugh', grin: 'laugh', joy: 'laugh', sad: 'cry', hurt: 'cry',
                dizzy: 'shock', scared: 'shock', surprise: 'shock', strain: 'angry', mad: 'angry', bored: 'deadpan', flat: 'deadpan' };
  const load = (key, src) => new Promise(r => { const i = new Image(); i.onload = () => { IM[key] = i; r(); }; i.onerror = () => r(); i.src = src; });
  function preload(names) {
    const p = Promise.all(names.flatMap(n => EX.concat(VIEWS).map(e => load(n + '/' + e, `${base}${n}/${e}.png`))));
    window.CAST_READY = p; return p;
  }
  const exprOf = e => EX.includes(e) ? e : (MAP[e] || 'smug');
  const get = (n, e) => IM[n + '/' + exprOf(e)];
  const has = n => !!IM[n + '/smug'];
  // The cut images are head + neck + collar; the head (hair top → chin) is the top ~78%.
  // Rig head circle radius R is centred at (0, -0.28R) in headFn space (same anchor the code portraits use).
  function head(ctx, n, e, fallback) {
    return (R, rigE) => {
      const im = get(n, typeof e === 'function' ? e() : (e || rigE));
      if (!im) { if (fallback) fallback(R, rigE); return; }
      const w = R * 2.45, h = w * im.height / im.width;
      ctx.drawImage(im, -w / 2, -R * 0.28 - h * 0.45, w, h);
    };
  }
  function face(ctx, n, e, x, y, size) { const im = get(n, e); if (!im) return false; const w = size, h = w * im.height / im.width; ctx.drawImage(im, x - w / 2, y - h / 2, w, h); return true; }
  function body(ctx, n, view, x, footY, height, flip) { const im = IM[n + '/' + view]; if (!im) return false; const h = height, w = h * im.width / im.height;
    ctx.save(); ctx.translate(x, footY); if (flip) ctx.scale(-1, 1); ctx.drawImage(im, -w / 2, -h, w, h); ctx.restore(); return true; }
  window.CASTIMG = { preload, head, face, body, get, has, EX, exprOf };
})();
