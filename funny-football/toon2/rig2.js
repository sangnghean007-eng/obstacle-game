// rig2.js — character upgrade layer (overhaul M2, 21 Nov 2026). Load after chibi.js (+ anim.js).
// Everything is a pure function of time, so parallel range rendering stays deterministic.
//  • RIG2.hand(...)          6 hand shapes: fist, open, point, thumb, grab, clap   → pass { hands: { f: 'point', b: 'fist' } } to chibi.draw
//  • RIG2.ragdoll(t, t0, opt) physical knock-back: returns { x, y, rot, pose } (bounces, rolls, limbs flop, settles)
//  • RIG2.motion(drawAt, t)  smear + ghost trail: draws the character at t-2dt, t-dt (faded) then at t
//  • RIG2.stretch(v)          squash/stretch factor from a speed (for o.sq)
//  • RIG2.flow(ctx, ...)      secondary motion strands (hair / scarf / shirt tail) that trail the movement (Verlet chain)
//  • RIG2.lips(env, t)        mouth shape from an audio envelope (lip sync)
(function () {
  const INK0 = '#22140c';
  function hand(ctx, x, y, r, skin, kind, ang, INK = INK0) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(-ang); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    const fill = (fn) => { ctx.beginPath(); fn(); ctx.fillStyle = skin; ctx.fill(); ctx.lineWidth = Math.max(3, r * 0.22); ctx.strokeStyle = INK; ctx.stroke(); };
    const finger = (fx, fy, len, a, w = r * 0.42) => { ctx.save(); ctx.translate(fx, fy); ctx.rotate(a); fill(() => ctx.roundRect(-w / 2, 0, w, len, w / 2)); ctx.restore(); };
    if (kind === 'fist') { fill(() => ctx.ellipse(0, r * 0.2, r * 1.05, r * 0.95, 0, 0, 7)); ctx.lineWidth = Math.max(2, r * 0.12); ctx.strokeStyle = 'rgba(0,0,0,.45)'; for (const k of [-0.5, 0, 0.5]) { ctx.beginPath(); ctx.moveTo(k * r, r * 0.6); ctx.lineTo(k * r, r * 0.95); ctx.stroke(); } }
    else if (kind === 'open') { for (const [a, l] of [[-0.55, 1.3], [-0.18, 1.6], [0.18, 1.55], [0.5, 1.3]]) finger(Math.sin(a) * r * 0.6, r * 0.4, r * l, -a); finger(-r * 0.8, 0, r * 1.1, 1.2); fill(() => ctx.ellipse(0, r * 0.3, r * 0.95, r * 0.85, 0, 0, 7)); }
    else if (kind === 'point') { fill(() => ctx.ellipse(0, r * 0.2, r, r * 0.9, 0, 0, 7)); finger(r * 0.15, r * 0.5, r * 1.9, 0, r * 0.46); finger(-r * 0.75, 0, r * 0.9, 0.9); }
    else if (kind === 'thumb') { finger(-r * 0.15, -r * 0.2, r * 1.7, Math.PI, r * 0.6); fill(() => ctx.ellipse(0, r * 0.3, r * 1.05, r * 0.9, 0, 0, 7)); ctx.strokeStyle = 'rgba(0,0,0,.4)'; ctx.lineWidth = Math.max(2, r * 0.1); for (const k of [0.1, 0.45, 0.8]) { ctx.beginPath(); ctx.moveTo(r * 0.2, r * (k - 0.1)); ctx.lineTo(r * 0.9, r * (k - 0.1)); ctx.stroke(); } }
    else if (kind === 'grab') { for (const a of [-0.6, -0.2, 0.2, 0.6]) finger(Math.sin(a) * r * 0.7, r * 0.5, r * 1.0, -a * 0.5 + 0.5); fill(() => ctx.ellipse(0, r * 0.2, r, r * 0.9, 0, 0, 7)); }
    else if (kind === 'clap') { fill(() => ctx.ellipse(0, r * 0.4, r * 0.7, r * 1.4, 0, 0, 7)); ctx.strokeStyle = 'rgba(0,0,0,.3)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, -r * 0.6); ctx.lineTo(0, r * 1.5); ctx.stroke(); }
    else if (kind === 'relax') { // cartoon hand: small palm, 4 long fingers side by side with a slight curl, thumb out to the side
      for (const [x, l, a] of [[-0.45, 1.45, 0.1], [-0.15, 1.7, 0.03], [0.15, 1.65, -0.03], [0.44, 1.35, -0.1]]) finger(x * r, r * 0.1, r * l, a, r * 0.36);
      finger(-r * 0.6, -r * 0.05, r * 1.15, 0.9, r * 0.4); fill(() => ctx.ellipse(0, r * 0.05, r * 0.72, r * 0.6, 0, 0, 7)); }
    else if (kind === 'wave') { for (const [a, l] of [[-0.6, 1.4], [-0.2, 1.7], [0.2, 1.65], [0.6, 1.4]]) finger(Math.sin(a) * r * 0.65, r * 0.4, r * l, -a * 1.2); finger(-r * 0.85, 0, r * 1.15, 1.4); fill(() => ctx.ellipse(0, r * 0.3, r * 0.95, r * 0.85, 0, 0, 7)); }
    else fill(() => ctx.ellipse(0, 0, r, r, 0, 0, 7));
    ctx.restore();
  }
  // deterministic ragdoll: rigid core (x, y, rot) + limb flop springs, integrated from t0 to t at fixed 1/240 s
  function ragdoll(t, t0, o = {}) {
    const g = o.g ?? 2600, e = o.bounce ?? 0.42, fr = o.friction ?? 0.82, gy = o.ground ?? 0, dt = 1 / 240;
    let x = o.x0 || 0, y = o.y0 || 0, vx = o.vx ?? 900, vy = o.vy ?? -1300, rot = o.rot0 || 0, vr = o.spin ?? 9; const L = { b: [0, 0], f: [0, 0], bl: [0, 0], fl: [0, 0] }, LV = { b: [0, 0], f: [0, 0], bl: [0, 0], fl: [0, 0] };
    const n = Math.max(0, Math.min(2400, Math.floor((t - t0) / dt))); let rest = false, bounces = 0;
    for (let i = 0; i < n; i++) {
      vy += g * dt; x += vx * dt; y += vy * dt; rot += vr * dt;
      if (y > gy) { y = gy; if (Math.abs(vy) > 120) { vy = -vy * e; vx *= fr; vr = vr * 0.6 + vx * 0.004; bounces++; } else { vy = 0; vx *= 0.9; vr *= 0.85; rot += (Math.round(rot / Math.PI) * Math.PI + (o.lieAngle ?? 1.5) - Math.round(rot / Math.PI) * Math.PI - rot) * 0.05; rest = Math.abs(vx) < 5; } }
      // limbs: driven by angular velocity + vertical acceleration (flop), damped springs to a flail target
      for (const k of ['b', 'f', 'bl', 'fl']) for (const j of [0, 1]) { const tgt = (k.length === 1 ? (k === 'b' ? -1 : 1) * 140 : (k === 'bl' ? -1 : 1) * 50) * (rest ? 0.4 : 1) - vr * 6 * (j + 1); const a = 80 * (tgt - L[k][j]) - 9 * LV[k][j]; LV[k][j] += a * dt; L[k][j] += LV[k][j] * dt; }
    }
    return { x, y, rot, rest, bounces, pose: { bArm: L.b, fArm: L.f, bLeg: L.bl, fLeg: L.fl } };
  }
  function motion(drawAt, t, n = 3, dt = 1 / 40, alpha = 0.18) { for (let k = n; k >= 1; k--) { const c = drawAt.ctx || window.ctx; c.save(); c.globalAlpha = alpha * (n - k + 1) / n; drawAt(t - k * dt, true); c.restore(); } drawAt(t, false); }
  const stretch = (v) => -Math.max(-0.22, Math.min(0.22, v / 6000));
  // Verlet chain (hair/scarf) anchored at an animated point; pure function of t (re-simulated from t-1 s)
  function flow(ctx, anchorAt, t, o = {}) {
    const N = o.n || 6, seg = o.len || 26, dt = 1 / 120, steps = 120; let P = []; const a0 = anchorAt(t - steps * dt);
    for (let i = 0; i < N; i++) P.push([a0[0] - i * seg * (o.dir || -1), a0[1] + i * 2, a0[0] - i * seg * (o.dir || -1), a0[1] + i * 2]);
    for (let s = steps; s >= 0; s--) { const a = anchorAt(t - s * dt); P[0][0] = P[0][2] = a[0]; P[0][1] = P[0][3] = a[1];
      for (let i = 1; i < N; i++) { const p = P[i]; const vx = (p[0] - p[2]) * 0.96, vy = (p[1] - p[3]) * 0.96; p[2] = p[0]; p[3] = p[1]; p[0] += vx + (o.wind || 0) * dt; p[1] += vy + 900 * dt * dt * 60 * (o.gravity ?? 0.25); }
      for (let it = 0; it < 3; it++) for (let i = 1; i < N; i++) { const p = P[i], q = P[i - 1]; const dx = p[0] - q[0], dy = p[1] - q[1], d = Math.hypot(dx, dy) || 1, k = (d - seg) / d; if (i > 1) { q[0] += dx * k * 0.5; q[1] += dy * k * 0.5; p[0] -= dx * k * 0.5; p[1] -= dy * k * 0.5; } else { p[0] -= dx * k; p[1] -= dy * k; } } }
    if (o.flutter ?? 1) for (let i = 1; i < N; i++) P[i][1] += Math.sin(t * 14 - i * 0.9) * 4 * i * (o.flutter ?? 1);
    ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    for (const [w, c] of [[(o.w || 18) + 8, o.ink || INK0], [o.w || 18, o.col || '#c8102e']]) { ctx.strokeStyle = c; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(P[0][0], P[0][1]); for (let i = 1; i < N; i++) ctx.lineTo(P[i][0], P[i][1]); ctx.stroke(); }
    ctx.restore(); return P;
  }
  function lips(env, t, fps = 60) { if (!env) return null; const v = env[Math.max(0, Math.min(env.length - 1, Math.round(t * fps)))] || 0; return v < 0.06 ? 'flat' : v < 0.2 ? 'smile' : v < 0.4 ? 'grin' : v < 0.65 ? 'shock' : 'yawn'; }
  window.RIG2 = { hand, ragdoll, motion, stretch, flow, lips };
})();
