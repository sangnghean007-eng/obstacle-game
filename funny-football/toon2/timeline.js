// timeline.js — write scenes as timelines instead of hand-coded coordinates (overhaul M3, 21 Nov 2026).
//   const tl = TL()
//     .set('ron', { x: 200, y: 1600, pose: 'stand', face: 'smug' })
//     .at(1.2).to('ron', { x: 700 }, 0.6, 'back')          // tween over 0.6 s with an ease
//     .at(1.8).hit('ron', { shake: 20, fx: 'dust', sound: 'thump' })
//     .at(2.0).say('ron', 'SIUUU', 1.2);
//   const S = tl.eval(t)   →  { ron: { x, y, pose, face, ... }, _events: [...active], _shake }
// Eases: linear, in, out, inout, back, elastic, bounce, snap. Pure function of t (parallel-render safe).
(function () {
  const E = { linear: k => k, in: k => k * k * k, out: k => 1 - (1 - k) ** 3, inout: k => k < 0.5 ? 4 * k * k * k : 1 - (-2 * k + 2) ** 3 / 2,
    back: k => { const c = 1.70158; return 1 + (c + 1) * (k - 1) ** 3 + c * (k - 1) ** 2; }, elastic: k => k === 0 || k === 1 ? k : 2 ** (-10 * k) * Math.sin((k * 10 - 0.75) * (2 * Math.PI / 3)) + 1,
    bounce: k => { const n = 7.5625, d = 2.75; if (k < 1 / d) return n * k * k; if (k < 2 / d) return n * (k -= 1.5 / d) * k + 0.75; if (k < 2.5 / d) return n * (k -= 2.25 / d) * k + 0.9375; return n * (k -= 2.625 / d) * k + 0.984375; }, snap: k => k < 1 ? 0 : 1 };
  function TL() {
    const init = {}, tw = [], ev = []; let cur = 0;
    const api = {
      set(id, props) { init[id] = Object.assign(init[id] || {}, props); return api; },
      at(t) { cur = t; return api; },
      to(id, props, dur = 0.5, ease = 'inout') { tw.push({ id, props, t0: cur, dur, ease }); return api; },
      pose(id, pose, face) { tw.push({ id, props: Object.assign({ pose }, face ? { face } : {}), t0: cur, dur: 0, ease: 'snap' }); return api; },
      hit(id, o = {}) { ev.push(Object.assign({ type: 'hit', id, t0: cur, dur: o.dur || 0.4 }, o)); return api; },
      say(id, text, dur = 1.2) { ev.push({ type: 'say', id, text, t0: cur, dur }); return api; },
      fx(kind, x, y, o = {}) { ev.push(Object.assign({ type: 'fx', kind, x, y, t0: cur, dur: o.dur || 2 }, o)); return api; },
      compile() { if (api._c) return; api._c = true; const done = []; // deterministic start values: value of each prop at the tween's start, from earlier tweens
        const valAt = (id, p, t) => { let v = init[id] ? init[id][p] : undefined; for (const w of done) { if (w.id !== id || !(p in w.props) || t < w.t0) continue; const k = w.dur ? Math.min(1, (t - w.t0) / w.dur) : 1, e = E[w.ease](k), to = w.props[p], fr = w.from[p]; v = (typeof to === 'number' && typeof fr === 'number') ? fr + (to - fr) * e : (k > 0 || w.dur === 0 ? to : fr); } return v; };
        for (const w of tw.slice().sort((a, b) => a.t0 - b.t0)) { w.from = {}; for (const p in w.props) w.from[p] = valAt(w.id, p, w.t0); done.push(w); } api._val = valAt; },
      eval(t) { api.compile(); const S = {}; const ids = new Set([...Object.keys(init), ...tw.map(w => w.id)]);
        for (const id of ids) { S[id] = Object.assign({}, init[id] || {}); for (const w of tw) if (w.id === id) for (const p in w.props) S[id][p] = api._val(id, p, t); }
        S._events = ev.filter(e => t >= e.t0 && t < e.t0 + e.dur).map(e => Object.assign({ k: (t - e.t0) / e.dur, age: t - e.t0 }, e));
        S._shake = S._events.filter(e => e.type === 'hit').reduce((m, e) => Math.max(m, (e.shake || 12) * (1 - e.k)), 0); return S; },
      events() { return ev.slice(); },
      length() { return Math.max(cur, ...tw.map(w => w.t0 + w.dur), ...ev.map(e => e.t0 + e.dur)); },
    };
    return api;
  }
  window.TL = TL; window.EASE = E;
})();
