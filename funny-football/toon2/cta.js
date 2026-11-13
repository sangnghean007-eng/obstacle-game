// Reusable end card: "+ FOLLOW" call to action (1.5 s). Platform-neutral (no app logos).
// Usage inside a scene file: ctaFollow(ctx, u, W, H, helpers) where u = seconds since the card started.
window.ctaFollow = function (ctx, u, W, H, h) {
  const { txt, rr, easeOutBack, clamp, CR, LM } = h;
  const g = ctx.createRadialGradient(W / 2, H * 0.45, 100, W / 2, H * 0.45, 1100); g.addColorStop(0, '#2a2f4a'); g.addColorStop(1, '#0b0e1c'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  CR('siu', 'grin', 300, 1650, 0.55); LM('sky', 'happy', 790, 1650, 0.5);
  // button pops, finger taps it at 0.55 s, button turns to "FOLLOWING ✓"
  const pop = easeOutBack(clamp(u / 0.25)), tapped = u > 0.6, press = u > 0.55 && u < 0.7 ? 0.92 : 1;
  ctx.save(); ctx.translate(W / 2, 560); ctx.scale(pop * press, pop * press);
  rr(-300, -90, 600, 180, 90, tapped ? '#16a34a' : '#e11d2a', '#1a0f08', 8);
  txt(tapped ? 'FOLLOWING ✓' : '+ FOLLOW', 0, 4, 88, '#fff', null); ctx.restore();
  // pointing hand
  const hx = W / 2 + 250, hy = 720 + (u < 0.55 ? (1 - clamp(u / 0.55)) * 300 : u < 0.7 ? -20 : 0);
  ctx.save(); ctx.translate(hx, hy); ctx.rotate(-0.4); rr(-36, -10, 72, 120, 30, '#f0c8a0', '#1a0f08', 6); rr(-14, -110, 28, 110, 14, '#f0c8a0', '#1a0f08', 6); ctx.restore();
  // ringing bell
  const ring = tapped ? Math.sin(u * 40) * 0.35 * Math.max(0, 1 - (u - 0.6) * 1.5) : 0;
  ctx.save(); ctx.translate(W / 2, 330); ctx.rotate(ring); ctx.beginPath(); ctx.moveTo(-60, 40); ctx.quadraticCurveTo(-60, -70, 0, -75); ctx.quadraticCurveTo(60, -70, 60, 40); ctx.lineTo(80, 60); ctx.lineTo(-80, 60); ctx.closePath();
  ctx.fillStyle = '#ffd60a'; ctx.fill(); ctx.lineWidth = 7; ctx.strokeStyle = '#1a0f08'; ctx.stroke(); ctx.beginPath(); ctx.arc(0, 72, 16, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); ctx.restore();
  txt('for more football roasts', W / 2, 760, 52, '#fff', '#1a0f08');
  txt('more episodes coming', W / 2, 840, 40, '#ffd60a', '#1a0f08');
};
