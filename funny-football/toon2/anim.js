// anim.js — "acting layer" for the chibi rig (Nov 20 2026, owner: "actions are stiff").
// The rig used to SNAP from one pose to the next. This wraps chibi.draw and, per character, adds:
//  • pose springs with slight overshoot (limbs swing into a pose and settle instead of teleporting)
//  • velocity-driven lean (leans into runs, leans back when braking)
//  • squash & stretch: stretches when moving fast vertically, squashes on landing, then springs back
//  • follow-through: the head lags a touch behind fast moves and wobbles back
// State is kept per character between consecutive frames (frames are rendered in order); a cut or a jump resets it.
(function () {
  const base = chibi.draw, ST = new Map(), LIMBS = ['bArm', 'fArm', 'bLeg', 'fLeg'];
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  function resolve(p) { return typeof p === 'string' ? (chibi.POSES[p] || null) : p; }
  function key(C, o) { return (C.name || '') + '|' + (C.skin || '') + '|' + (C.num || '') + '|' + ((C.head && C.head.hair) || '') + '|' + (o && o.animKey || ''); }
  chibi.draw = function (c2d, C, pose, expr, x, y, s, o = {}) {
    if (o.noAnim) return base(c2d, C, pose, expr, x, y, s, o);
    const t = window.T2T || 0, P = resolve(pose); const k = key(C, o); let S = ST.get(k);
    const fresh = !S || t <= S.t || t - S.t > 0.12 || Math.hypot(x - S.x, y - S.y) > 260 * Math.max(0.5, s);
    if (fresh || !P) { S = { t, x, y, vx: 0, vy: 0, sq: 0, sqv: 0, tilt: 0, tiltv: 0, p: P ? JSON.parse(JSON.stringify(P)) : null, pv: { bArm: [0, 0], fArm: [0, 0], bLeg: [0, 0], fLeg: [0, 0] } }; ST.set(k, S); return base(c2d, C, pose, expr, x, y, s, o); }
    const dt = Math.min(1 / 30, t - S.t);
    // pose springs (stiff, slightly under-damped → small overshoot)
    const K = o.snap ? 2600 : 1300, D = o.snap ? 60 : 42; const out = {};
    for (const L of LIMBS) { out[L] = [0, 0]; for (let i = 0; i < 2; i++) { const target = P[L] ? P[L][i] : 0; let cur = S.p[L] ? S.p[L][i] : target; let v = S.pv[L][i]; const a = K * (target - cur) - D * v; v += a * dt; cur += v * dt; S.p[L] = S.p[L] || [0, 0]; S.p[L][i] = cur; S.pv[L][i] = v; out[L][i] = cur; } }
    // velocity (smoothed)
    const nvx = (x - S.x) / dt, nvy = (y - S.y) / dt; const pvy = S.vy; S.vx += (nvx - S.vx) * 0.35; S.vy += (nvy - S.vy) * 0.5;
    // landing squash impulse: was falling fast, now stopped
    if (pvy > 900 && Math.abs(nvy) < 200) S.sqv += Math.min(14, pvy / 160);
    // squash spring (target = stretch from vertical speed)
    const sqT = -clamp(Math.abs(S.vy) / 5200, 0, 0.16); const sa = 420 * (sqT - S.sq) - 16 * S.sqv; S.sqv += sa * dt; S.sq += S.sqv * dt;
    // follow-through tilt of the head/body against horizontal acceleration
    const ta = 300 * (clamp(-S.vx / 9000, -0.12, 0.12) - S.tilt) - 14 * S.tiltv; S.tiltv += ta * dt; S.tilt += S.tiltv * dt;
    S.t = t; S.x = x; S.y = y;
    const lean = (o.lean || 0) + clamp(S.vx / 6500, -0.22, 0.22) * (o.f || 1) * (o.f === -1 ? -1 : 1);
    const o2 = Object.assign({}, o, { lean, sq: (o.sq || 0) + clamp(S.sq, -0.2, 0.3), headTilt: (o.headTilt || 0) + S.tilt });
    return base(c2d, C, out, expr, x, y, s, o2);
  };
})();
