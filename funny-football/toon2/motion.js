// motion.js — motion lessons adapted from Remotion's official agent skills (read 24 Nov 2026, remotion-dev/skills: timing, transitions,
// light-leaks, motion-blur) into our plain-canvas engine. No Remotion dependency.
//   MOTION.spring(k, {damping, stiffness})  damped-spring ease 0→1 (overshoot + settle), like Easing.spring
//   MOTION.interp(t, [t0,t1], [a,b], ease)  clamped interpolate()
//   MOTION.cut(ctx, t, tCut, kind)          transition overlay ON the cut point (does not shorten the timeline):
//        'whip'  horizontal whip-pan streaks · 'flash' white pop · 'leak' warm light leak · 'iris' black iris close/open
//   MOTION.blurTrail(draw, t, n, span)      cheap motion blur for one fast object: draws it n times at earlier times, fading
(function () {
  const W = 1080, H = 1920, clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const M = {
    spring(k, o = {}) { k = clamp(k); const d = o.damping ?? 9, w = o.stiffness ?? 14; return 1 - Math.exp(-d * k) * Math.cos(w * k); },
    interp(t, [t0, t1], [a, b], ease = x => x) { return a + (b - a) * ease(clamp((t - t0) / (t1 - t0))); },
    cut(ctx, t, tc, kind = 'whip', dur = 0.32) { const q = (t - (tc - dur / 2)) / dur; if (q < 0 || q > 1) return; const p = 1 - Math.abs(q * 2 - 1);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
      if (kind === 'whip') { ctx.globalAlpha = p * 0.9; for (let i = 0; i < 34; i++) { const y = (i * 151) % H, len = 300 + (i * 97) % 700, x = ((q * 2600 + i * 211) % (W + len)) - len;
          ctx.fillStyle = i % 3 ? 'rgba(255,255,255,.75)' : 'rgba(20,20,30,.6)'; ctx.fillRect(x, y, len, 10 + (i % 4) * 8); }
        ctx.globalAlpha = p * 0.35; ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); }
      if (kind === 'flash') { ctx.globalAlpha = p * p; ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); }
      if (kind === 'leak') { ctx.globalCompositeOperation = 'screen'; const g = ctx.createRadialGradient(W * (0.2 + q * 0.7), H * 0.35, 40, W * (0.2 + q * 0.7), H * 0.35, 1100);
        g.addColorStop(0, `rgba(255,190,90,${0.95 * p})`); g.addColorStop(0.45, `rgba(255,80,60,${0.5 * p})`); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); }
      if (kind === 'iris') { const r = Math.max(0, 1 - p) * 1200; ctx.fillStyle = '#000'; ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.arc(W / 2, H * 0.45, r, 0, 7, true); ctx.fill('evenodd'); }
      ctx.restore(); },
    blurTrail(draw, t, n = 5, span = 0.06) { const ctx = window.ctx; for (let i = n; i >= 1; i--) { ctx.save(); ctx.globalAlpha = 0.5 * (1 - i / (n + 1)); draw(t - span * i / n); ctx.restore(); } draw(t); }
  };
  window.MOTION = M;
})();
