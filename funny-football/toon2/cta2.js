// cta2.js — end-of-video support call (owner 24 Nov 2026: "quên kêu gọi sự ủng hộ … ở cuối video").
// Overlay on the last ~2.4 s (does not cut away, so the loop survives). A finger taps 👍 LIKE → 🔔 FOLLOW → ↗ SHARE; each turns "done".
//   CTA2.draw(ctx, u, { y, line, font })   u = seconds since the overlay started (0…2.4)
// Sound (audio.py): CTA2 timing → taps at u = 0.45, 1.0, 1.55 (use fx2: m.cta(t0)).  Every episode MUST call CTA2.draw (post_gate checks it).
(function () {
  const W = 1080, clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v)), back = k => { k = clamp(k); const c = 1.7; return 1 + (c + 1) * (k - 1) ** 3 + c * (k - 1) ** 2; };
  const BTN = [['👍', 'LIKE', '#1d4ed8'], ['🔔', 'FOLLOW', '#e11d2a'], ['↗', 'SHARE', '#16a34a']], TAP = [0.45, 1.0, 1.55];
  window.CTA2 = { TAP, DUR: 2.4,
    draw(ctx, u, o = {}) { if (u < 0) return; const y = o.y ?? 1420, F = o.font || '"Bangers","Impact",sans-serif';
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); const k = back(u / 0.3);
      ctx.globalAlpha = clamp(u / 0.15); ctx.fillStyle = 'rgba(10,12,28,.82)'; ctx.beginPath(); ctx.roundRect(40, y - 120 + (1 - k) * 80, W - 80, 280, 40); ctx.fill();
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = `400 50px ${F}`; ctx.fillStyle = '#ffd23f'; ctx.fillText(o.line || 'Follow for more 🍿', W / 2, y - 62);
      BTN.forEach(([ic, lab, col], i) => { const x = 200 + i * 340, done = u > TAP[i] + 0.08, press = u > TAP[i] && u < TAP[i] + 0.14 ? 0.88 : 1, pk = back((u - 0.1 - i * 0.08) / 0.3);
        ctx.save(); ctx.translate(x, y + 50); ctx.scale(pk * press, pk * press); ctx.fillStyle = done ? '#ffffff' : col; ctx.strokeStyle = '#000'; ctx.lineWidth = 6; ctx.beginPath(); ctx.roundRect(-150, -58, 300, 116, 58); ctx.fill(); ctx.stroke();
          ctx.font = `400 50px ${F}`; ctx.fillStyle = done ? col : '#fff'; ctx.fillText((done ? '✓ ' : ic + ' ') + lab, 0, 4);
          if (done && u < TAP[i] + 0.6) { const q = (u - TAP[i]) / 0.6; ctx.strokeStyle = col; ctx.globalAlpha = 1 - q; ctx.lineWidth = 8; ctx.beginPath(); ctx.roundRect(-150 - q * 40, -58 - q * 30, 300 + q * 80, 116 + q * 60, 70); ctx.stroke(); } ctx.restore(); });
      // the tapping finger travels button to button
      const seg = TAP.findIndex(a => u < a + 0.2), i = seg < 0 ? 2 : seg, prev = Math.max(0, i - 1), t0 = i ? TAP[prev] + 0.2 : 0, q = clamp((u - t0) / Math.max(0.01, TAP[i] - t0));
      const fx = (i ? 200 + prev * 340 : 200) + ((200 + i * 340) - (i ? 200 + prev * 340 : 200)) * q + 60, fy = y + 120 - (u > TAP[i] - 0.05 && u < TAP[i] + 0.12 ? 25 : 0) + (i === 0 ? (1 - q) * 200 : 0);
      ctx.translate(fx, fy); ctx.rotate(-0.35); ctx.fillStyle = '#f0c8a0'; ctx.strokeStyle = '#1a0f08'; ctx.lineWidth = 6; ctx.beginPath(); ctx.roundRect(-34, 0, 68, 110, 28); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.roundRect(-13, -90, 26, 100, 13); ctx.fill(); ctx.stroke();
      ctx.restore(); } };
})();
