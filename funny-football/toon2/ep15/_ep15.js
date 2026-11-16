// ================= Episode 15: "DON'T MESS WITH CR7 🏆" — Yamal mocks Ronaldo (Messi has a World Cup, you have zero) → the TROPHY COMBO → Yamal runs to Rodri → showdown with a giant World Cup.
// Real titles only: CR7 Euro 2016, Nations League 2019 + 2025 (beat Spain/Yamal in the 2025 final), 5 UCL, 5 Ballon d'Or, 0 World Cups; Messi WC 2022; Rodri = Spain captain + Golden Ball at the 2026 World Cup. Everything else = cartoon parody.
CAST.rodri = ['rodri', ESPK, '16', 'RODRI', '#e3b08c'];
const YA = (pose, ex, x, y, s = 0.95, o = {}) => PL('yamal', x, y, s, pose, ex, o);
const RD = (pose, ex, x, y, s = 1.0, o = {}) => PL('rodri', x, y, s, pose, ex, o);
const GYS = 1480; const AKIMBO = { bArm: [-35, 25], fArm: [35, -25], bLeg: [-12, -6], fLeg: [12, 6] };
function street(t, tint) { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, tint ? '#f6c27a' : '#8fd3ff'); g.addColorStop(1, tint ? '#f9e1b0' : '#e8f6ff'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, 1250);
  for (let i = 0; i < 5; i++) { const x = i * 230 - 40, h = 380 + (i % 3) * 90; rr(x, 1250 - h, 210, h, 6, tint ? ['#d9a066', '#c98a52', '#e0b07a'][i % 3] : ['#f2d7b6', '#e8c49e', '#f5e3cc'][i % 3], DARK, 4); for (let r = 0; r < 4; r++) for (let c = 0; c < 2; c++) rr(x + 30 + c * 90, 1250 - h + 40 + r * 80, 56, 48, 6, '#7fb2d9', DARK, 3); }
  ctx.fillStyle = tint ? '#c9a06a' : '#9a9a9a'; ctx.fillRect(0, 1250, W, 120); ctx.fillStyle = tint ? '#b48a55' : '#7b7b7b'; ctx.fillRect(0, 1370, W, 600); ctx.strokeStyle = 'rgba(255,255,255,.5)'; ctx.lineWidth = 6; ctx.setLineDash([60, 40]); ctx.beginPath(); ctx.moveTo(0, 1600); ctx.lineTo(W, 1600); ctx.stroke(); ctx.setLineDash([]); }
function home(t) { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#2a3f6a'); g.addColorStop(1, '#4a3a5a'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.fillStyle = '#3a2a3a'; ctx.fillRect(0, 1380, W, 600); rr(640, 560, 340, 420, 12, '#c60b1e', '#ffc400', 10); txt('ESPAÑA', 810, 640, 50, '#ffc400', null); txt('🏆 2026', 810, 760, 70, '#fff', null); }
function phone(x, y, k) { pop(eOB(k / 0.15), x, y, () => { ctx.rotate(-0.1); rr(-110, -200, 220, 400, 26, '#111', DARK, 6); ctx.save(); ctx.beginPath(); ctx.roundRect(-96, -180, 192, 360, 18); ctx.clip(); ctx.fillStyle = '#1b2a5c'; ctx.fillRect(-96, -180, 192, 360); face('messi', 0, 10, 0.33, 'smug', '#74acdf'); worldCup(55, 150, 0.55, 1); ctx.restore(); rr(-80, 140, 160, 34, 8, 'rgba(0,0,0,.6)', null); txt('2022 🏆', 0, 157, 24, '#ffd60a', null); }); }
function trunk(x, y, open) { rr(x - 170, y - 200, 340, 200, 16, '#6b3f1f', DARK, 7); for (const d of [-110, 110]) rr(x + d - 10, y - 200, 20, 200, 4, '#d4a017', null); ctx.save(); ctx.translate(x - 170, y - 200); ctx.rotate(-open * 1.4); rr(0, -60, 340, 60, 14, '#7a4a26', DARK, 7); ctx.restore(); txt('CR7 MUSEUM', x, y - 100, 30, '#ffd60a', DARK); if (open > 0.5) { const g = ctx.createRadialGradient(x, y - 220, 10, x, y - 220, 220); g.addColorStop(0, 'rgba(255,230,120,.8)'); g.addColorStop(1, 'rgba(255,230,120,0)'); ctx.fillStyle = g; ctx.fillRect(x - 220, y - 440, 440, 300); } }
function euroCup(x, y, s = 1) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); rr(-40, -20, 80, 22, 6, '#9ca3af', DARK, 5); ctx.beginPath(); ctx.moveTo(-50, -170); ctx.quadraticCurveTo(-56, -40, 0, -22); ctx.quadraticCurveTo(56, -40, 50, -170); ctx.closePath(); ctx.fillStyle = '#e5e7eb'; ctx.fill(); ctx.lineWidth = 6; ctx.strokeStyle = DARK; ctx.stroke(); for (const d of [-1, 1]) { ctx.beginPath(); ctx.moveTo(d * 48, -150); ctx.bezierCurveTo(d * 100, -160, d * 100, -80, d * 40, -80); ctx.stroke(); } txt('EURO', 0, -100, 24, DARK, null); ctx.restore(); }
function nlCup(x, y, s = 1) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); rr(-34, -24, 68, 26, 6, '#6b7280', DARK, 5); ctx.beginPath(); ctx.moveTo(-26, -24); ctx.lineTo(-44, -190); ctx.lineTo(44, -190); ctx.lineTo(26, -24); ctx.closePath(); ctx.fillStyle = '#d1d5db'; ctx.fill(); ctx.lineWidth = 6; ctx.strokeStyle = DARK; ctx.stroke(); txt('NL', 0, -110, 28, DARK, null); ctx.restore(); }
function lumps(x, y, n, s = 1) { for (let i = 0; i < n; i++) { ell(x + ((i % 3) - 1) * 18 * s, y - i * 26 * s, 26 * s - i * 0.6, 18 * s, '#f0b090', 4); ell(x + ((i % 3) - 1) * 18 * s - 6, y - i * 26 * s - 6, 7 * s, 4 * s, 'rgba(255,255,255,.6)'); } }
function tears(x, y, t, k = 1) { for (const d of [-1, 1]) for (let i = 0; i < 10; i++) { const q = ((t * 2.2 + i / 10) % 1); ell(x + d * (20 + q * 160 * k), y + q * q * 260 - q * 40, 9, 12, `rgba(120,200,255,${1 - q})`); } }
function tumble(x, y, t) { ctx.save(); ctx.translate(x, y); ctx.rotate(t * 4); ctx.strokeStyle = '#8b6a3a'; ctx.lineWidth = 5; for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.arc(Math.sin(i) * 10, Math.cos(i * 1.3) * 10, 30 + (i % 3) * 10, i, i + 3.5); ctx.stroke(); } ctx.restore(); }
function cart(x, y) { rr(x - 200, y - 70, 400, 50, 10, '#8b5a2b', DARK, 6); for (const d of [-150, 150]) { ell(x + d, y - 12, 26, 26, '#333', 5); ell(x + d, y - 12, 8, 8, '#999'); } }
// a trophy swung from CR7's hand onto Yamal's head
function swing(drawFn, z, t0, dur, from, to, label = 'BONK!') { const k = (z - t0) / dur; if (k < 0 || k > 1.5) return false; const e = easeIO(clamp(k)); ctx.save(); ctx.translate(lerp(from[0], to[0], e), lerp(from[1], to[1], e) - Math.sin(e * Math.PI) * 220); ctx.rotate(lerp(-0.6, 1.3, e)); drawFn(); ctx.restore(); swoosh(from[0], from[1], to[0], to[1], clamp(k)); if (k > 0.9) burst(to[0], to[1] - 60, 110, label, (k - 0.9) / 0.1, 44, '#fff'); return k > 0.9; }

// ---------- shots ----------
function s_hook(z, t) { street(t); const hit = z > 1.2; const yx = hit ? 520 - Math.min(140, (z - 1.2) * 400) : lerp(-100, 520, clamp(z / 1.2));
  RO(AKIMBO, hit ? 'deadpan' : 'neutral', 720, GYS, 0.95, { f: -1 });
  YA(hit ? P_HIT : runPose(t, 8), hit ? 'shock' : 'smug', yx, GYS, 0.95, { rot: hit ? -0.2 * Math.max(0, 1 - (z - 1.2) * 2) : 0 }); if (!hit || z < 1.6) shades(yx, GYS - 0.95 * 375, 0.95); else { const k = clamp((z - 1.2) / 0.5); shades(yx - k * 120, GYS - 0.95 * 375 - k * 200 + k * k * 260, 0.95, -k * 6); }
  if (hit && z < 1.6) burst(620, 1120, 110, 'BONK', (z - 1.2) / 0.1, 40, '#fff');
  if (z > 1.8) bubble('watch it, old man 😏', 400, 960, z - 1.8, 42); }
function s_mock(z, t) { street(t); RO(AKIMBO, z > 2.6 ? 'angry' : 'deadpan', 720, GYS, 0.95, { f: -1 });
  const laugh = z > 3.0; YA(laugh ? { bArm: [-60, -150], fArm: [60, 150], bLeg: [-12, -6], fLeg: [12, 6] } : { bArm: [-20, -10], fArm: [100, 150], bLeg: [-8, -4], fLeg: [8, 4] }, laugh ? 'siuuu' : 'smug', 380, GYS + (laugh ? -Math.abs(Math.sin(t * 14)) * 12 : 0), 0.95);
  if (z < 3.0) phone(560, 960, z - 0.2); if (z > 0.6 && z < 3.0) bubble('Messi has a World Cup… 🏆', 360, 760, z - 0.6, 40);
  if (z > 3.0) { pop(eOB((z - 3.0) / 0.15), 380, 900, () => { ell(0, 0, 90, 110, null, 22); ctx.lineWidth = 22; ctx.strokeStyle = '#fff'; ctx.beginPath(); ctx.ellipse(0, 0, 80, 100, 0, 0, TAU); ctx.stroke(); }); bubble('…you have ZERO 😂', 360, 760, z - 3.0, 46); tears(380, 1110, t, 0.4); }
  if (z > 2.6) { steam2(720, 1020, t); txt('💢', 790, 1000, 60, '#fff', null); } }
const COMBO = [ // [t0, dur, draw, label, add]
  [1.0, 0.45, () => euroCup(0, 0, 0.8), 'EURO 2016', 1], [3.4, 0.4, () => nlCup(0, 0, 0.8), 'NATIONS LEAGUE 2019', 1], [4.2, 0.4, () => nlCup(0, 0, 0.8), 'NATIONS LEAGUE 2025', 1],
  [6.6, 0.3, () => uclCup(0, 0, 0.6, 0), 'UCL', 1], [7.0, 0.3, () => uclCup(0, 0, 0.6, 0), 'UCL', 1], [7.4, 0.3, () => uclCup(0, 0, 0.6, 0), 'UCL', 1], [7.8, 0.3, () => uclCup(0, 0, 0.6, 0), 'UCL', 1], [8.2, 0.3, () => uclCup(0, 0, 0.6, 0), 'UCL', 1]];
function s_combo(z, t) { street(t); trunk(860, GYS + 20, clamp((z - 0.2) / 0.4));
  let hits = 0; for (const [t0, dur, , , add] of COMBO) if (z > t0 + dur * 0.9) hits += add; const bdo = z > 10.6 ? Math.min(5, Math.floor((z - 10.6) / 0.35) + 1) : 0; hits += bdo;
  const spin = z > 6.6 && z < 9.2; const dazed = hits > 0; const yx = 380;
  YA(spin ? FLAIL(t) : dazed ? P_HIT : 'stand', dazed ? 'shock' : 'smug', yx, GYS, 0.95, { rot: spin ? Math.sin(t * 25) * 0.25 : 0, f: spin && Math.sin(t * 25) > 0 ? -1 : 1 });
  if (hits < 1) shades(yx, GYS - 0.95 * 375, 0.95); const headY = GYS - 0.95 * 500; lumps(yx + 10, headY, Math.min(hits, 13), 1); if (dazed) stars(yx, headY - 40 - Math.min(hits, 13) * 26, t, 80);
  const swingIt = COMBO.some(([t0, dur]) => z > t0 - 0.1 && z < t0 + dur + 0.2) || (z > 10.4 && z < 12.4);
  RO(swingIt ? { bArm: [-20, -10], fArm: [150, 170], bLeg: [-14, -8], fLeg: [14, 8] } : z > 12.8 ? RAISE : AKIMBO, z > 12.8 ? 'siuuu' : 'smug', 680, GYS, 0.95, { f: -1 });
  for (const [t0, dur, draw, label] of COMBO) swing(draw, z, t0, dur, [640, 900], [yx + 10, headY + 20], 'BONK!');
  if (z > 10.4 && z < 12.6) for (let i = 0; i < 5; i++) { const k = clamp((z - 10.4 - i * 0.35) / 0.4); if (k > 0 && k < 1) ballonDor(lerp(560 + i * 30, yx + 10, k), lerp(600, headY, k * k), 0.9, 1); }
  if (z > 2.9 && z < 5.2) bubble('June 2025… I beat YOU in the final 😏', 660, 820, z - 2.9, 34);
  if (z > 12.8) bubble('SIUUU 😎', 680, 900, z - 12.8, 50);
  HUD(() => { if (hits > 0) pop(1 + (hits && (z % 0.4) < 0.1 ? 0.12 : 0), W / 2, 300, () => { rr(-330, -70, 660, 140, 30, 'rgba(10,14,30,.9)', '#ffd60a', 6); txt(`TROPHY COMBO ×${hits}`, 0, 4, 60, '#ffd60a', null); });
    const cur = COMBO.filter(([t0]) => z > t0 - 0.2).pop(); const lab = z > 10.4 ? "BALLON D'OR ×5 ✨" : z > 6.4 ? 'CHAMPIONS LEAGUE ×5 ⭐' : cur ? cur[3] : ''; if (lab && z < 12.8) caption(lab, 0.5, 440, '#111', '#fff', 46); }); }
function s_cry(z, t) { street(t); const run = z > 1.6; const yx = run ? lerp(380, -350, easeIO((z - 1.6) / 2.2)) : 380;
  RO(z > 2.2 ? RAISE : AKIMBO, z > 2.2 ? 'siuuu' : 'smug', 720, GYS, 0.95, { f: -1 }); if (z > 2.2) bubble('SIUUU 😎', 720, 880, z - 2.2, 46);
  YA(run ? runPose(t, 22) : { bArm: [-160, -130], fArm: [160, 130], bLeg: [-8, -4], fLeg: [8, 4] }, 'shock', yx, GYS, 0.95, { f: run ? -1 : 1, rot: run && z > 2.4 && z < 2.7 ? -0.6 : 0 }); lumps(yx + 10, GYS - 0.95 * 500, 13, 1); tears(yx, GYS - 0.95 * 360, t, 1);
  if (run) for (let i = 0; i < 5; i++) ell(yx + 120 + i * 50, GYS - 20 + Math.sin(t * 9 + i) * 8, 40 - i * 5, 22, 'rgba(220,210,190,.8)');
  if (z > 0.3 && z < 3.2) bubble("I'M TELLING RODRI! 😭", 420, 820, z - 0.3, 44); if (z > 2.4 && z < 2.8) burst(yx, GYS - 80, 90, 'TRIP', (z - 2.4) / 0.1, 34, '#fff'); }
function s_rodri(z, t) { home(t); const hug = z < 3.2;
  RD(z > 3.0 ? { bArm: [-30, -10], fArm: [110, 160], bLeg: [-12, -6], fLeg: [12, 6] } : 'stand', z > 2.4 ? 'angry' : 'deadpan', 420, 1440, 1.0);
  YA(hug ? { bArm: [60, 100], fArm: [70, 110], bLeg: [80, 0], fLeg: [90, 0] } : { bArm: [-20, -10], fArm: [120, 150], bLeg: [-8, -4], fLeg: [8, 4] }, 'shock', hug ? 300 : 220, 1500, 0.8, { f: 1 }); lumps(hug ? 310 : 230, 1500 - 0.8 * 500, 13, 0.85); if (hug) tears(300, 1500 - 0.8 * 360, t, 0.7);
  if (z > 0.3 && z < 2.2) bubble('he hit me with 13 trophies 😭', 330, 880, z - 0.3, 36); if (z > 2.0 && z < 2.6) txt('*sigh*', 470, 900, 40, '#fff', DARK); if (z > 2.4 && z < 3.0) burst(520, 1100, 80, 'CRACK', (z - 2.4) / 0.1, 32, '#fff');
  const wk = clamp((z - 3.2) / 1.6); if (wk > 0) { const cx = lerp(1300, 820, easeOut(wk)); cart(cx, 1500); worldCup(cx, 1440, 2.4, 1); pop(eOB((z - 3.6) / 0.15), cx, 760, () => { rr(-230, -80, 460, 160, 20, 'rgba(0,0,0,.75)', '#ffd60a', 5); txt('WORLD CUP 2026', 0, -26, 40, '#ffd60a', null); txt('CAPTAIN · GOLDEN BALL', 0, 30, 30, '#fff', null); }); }
  if (z > 4.6) bubble('show me 😤', 420, 840, z - 4.6, 50); }
function s_showdown(z, t) { street(t, true); tumble(lerp(1200, -150, (z * 0.18) % 1), 1440, t);
  // CR7's little pile
  euroCup(820, GYS + 10, 0.5); nlCup(870, GYS + 10, 0.45); nlCup(910, GYS + 10, 0.45); for (let i = 0; i < 3; i++) uclCup(780 + i * 50, GYS - 60, 0.3, 0);
  const land = z > 2.4; const tx = land ? 560 : lerp(-300, 560, clamp(z / 2.2)); const ty = land ? GYS : GYS - 60;
  if (!land) { cart(tx, GYS); RD(runPose(t, 6), 'angry', tx - 260, GYS, 1.0); YA('stand', 'smug', tx - 380, GYS + 10, 0.75); }
  const wink = z > 7.0; if (!wink) worldCup(tx, ty, land ? 3.0 : 2.8, 1); else cup(tx, ty, 3.0, t, { legs: false, look: 1, mood: z > 7.6 ? null : null });
  if (wink && z < 7.4) { ctx.fillStyle = '#d4a017'; ctx.fillRect(tx - 45, ty - 3.0 * 252, 90, 34); }
  if (land && z < 2.9) burst(tx, GYS - 40, 200, 'THOOM', (z - 2.4) / 0.1, 60, '#fff');
  if (land) { ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.beginPath(); ctx.ellipse(780, GYS + 10, 260, 40, 0, 0, TAU); ctx.fill(); RD(AKIMBO, 'smug', 250, GYS, 1.0); YA({ bArm: [-20, -10], fArm: [100, 130], bLeg: [-8, -4], fLeg: [8, 4] }, 'smug', 120, GYS + 20, 0.8, { f: 1 }); lumps(130, GYS + 20 - 0.8 * 500, 6, 0.85); }
  const climb = z > 4.6 && z < 6.8; const cy = climb ? GYS - Math.max(0, Math.sin(clamp((z - 4.6) / 1.4) * Math.PI) * 360) : GYS;
  RO(climb ? JUMPP : wink ? { bArm: [-40, -20], fArm: [40, 20], bLeg: [-12, -6], fLeg: [12, 6] } : 'stand', wink ? 'shock' : climb ? 'angry' : 'deadpan', climb ? 760 : 860, cy, 0.95, { f: -1 });
  if (z > 3.0 && z < 4.6) bubble('count THIS one 😏', 280, 880, z - 3.0, 40); if (z > 3.6 && z < 4.8) bubble('ZERO 😝', 150, 1140, z - 3.6, 38);
  if (z > 6.0 && z < 6.6) burst(700, GYS - 200, 90, 'SKRRT', (z - 6.0) / 0.1, 32, '#fff');
  if (wink) bubble('still RESERVED? 😏', 600, 560, z - 7.2, 44); if (z > 8.0) txt('😱', 940, 990, 80, '#fff', null); }
function s_twist(z, t) { street(t, true); worldCup(560, GYS, 3.0, 1); RD(AKIMBO, z > 1.8 ? 'shock' : 'smug', 250, GYS, 1.0); YA('stand', z > 1.8 ? 'shock' : 'smug', 120, GYS + 20, 0.8, { f: 1 });
  RO({ bArm: [-20, -10], fArm: [150, 160], bLeg: [-12, -6], fLeg: [12, 6] }, z > 1.0 ? 'smug' : 'deadpan', 860, GYS, 0.95, { f: -1 });
  pop(eOB((z - 0.5) / 0.15), 860, 820, () => { rr(-90, -150, 180, 300, 22, '#111', DARK, 5); ctx.fillStyle = '#1b2a5c'; ctx.fillRect(-78, -136, 156, 272); txt('calling…', 0, -90, 26, '#fff', null); txt('MESSI', 0, -40, 38, '#74acdf', null); txt('📞', 0, 40, 60, '#fff', null); });
  HUD(() => { if (z > 1.6) title('TO BE CONTINUED…', z - 1.6, 300, 66, '#fff'); if (z > 2.4) pop(eOB((z - 2.4) / 0.15), W / 2, 440, () => { rr(-420, -60, 840, 120, 30, '#fff', DARK, 6); txt('Who wins this beef? 7 · 19 · 16 👇', 0, 4, 42, DARK, null); });
    rr(70, 1500, 940, 64, 32, 'rgba(0,0,0,.55)', null); txt('Real titles · cartoon parody', W / 2, 1533, 34, '#fff', null, 'center', 800); }); }

// ---------- camera + HUD ----------
let HUDQ = []; const HUD = (f) => HUDQ.push(f);
const _cap = caption; caption = (...a) => HUD(() => _cap(...a));
const N = (t) => [t, 540, 960, 1];
const CAMS = { hook: [[0, 540, 1150, 1.15], [1.1, 580, 1150, 1.25], [1.4, 600, 1150, 1.4], [3.4, 520, 1120, 1.3]], mock: [[0, 500, 1100, 1.2], [2.8, 460, 1050, 1.35], [3.2, 450, 1050, 1.45], [6.0, 520, 1100, 1.3]],
  combo: [[0, 600, 1150, 1.15], [1.6, 520, 1100, 1.25], [6.4, 520, 1100, 1.25], [7.0, 420, 1050, 1.5], [9.2, 420, 1050, 1.5], [10.2, 480, 1000, 1.25], [12.6, 440, 1000, 1.35], [15.0, 560, 1100, 1.2]],
  cry: [[0, 420, 1050, 1.4], [1.6, 420, 1050, 1.4], [2.2, 540, 1100, 1.1], [5.0, 540, 1100, 1.1]], rodri: [[0, 380, 1200, 1.3], [3.0, 400, 1150, 1.3], [3.4, 600, 1100, 1.0], [6.0, 600, 1100, 1.05]],
  showdown: [[0, 540, 1100, 1.0], [2.3, 540, 1100, 1.0], [2.6, 500, 1000, 1.05], [4.4, 400, 1100, 1.2], [5.0, 700, 1150, 1.2], [6.8, 700, 1150, 1.2], [7.2, 520, 800, 1.25], [10.0, 600, 900, 1.25]], twist: [[0, 600, 1100, 1.1], [5.0, 600, 1050, 1.15]] };
const SHK = { hook: [[1.2, 0.3, 14]], mock: [], combo: [[1.4, 0.2, 12], [3.75, 0.2, 12], [4.55, 0.2, 12], [6.85, 2.0, 10], [10.6, 1.8, 10]], cry: [[2.4, 0.2, 8]], rodri: [[2.4, 0.2, 8]], showdown: [[2.4, 0.5, 22], [7.0, 0.3, 10]], twist: [] };
const shakeAt = (n, z) => SHK[n].reduce((m, [a, d, A]) => z >= a && z < a + d ? Math.max(m, A * (1 - (z - a) / d)) : m, 0);
const LEN = [['hook', 3.4, s_hook, 1], ['mock', 6.0, s_mock, 1], ['combo', 15.0, s_combo, 1], ['cry', 5.0, s_cry, 1], ['rodri', 6.0, s_rodri, 1], ['showdown', 10.0, s_showdown, 1], ['twist', 5.0, s_twist, 1]];
const SEG = []; { let t = 0; for (const [n, d, f, sl] of LEN) { SEG.push([t, t + d * sl, f, n, sl]); t += d * sl; } }
const DURATION = SEG[SEG.length - 1][1];
window.SEGS = SEG.map(s => [s[3], +s[0].toFixed(2)]);
function render(t) { ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H); window.T2T = t;
  for (const [a, b, fn, n, sl] of SEG) if (t >= a && t < b) { const z = (t - a) / sl; HUDQ = []; const sh = shakeAt(n, z), C = camK(CAMS[n], z); C[2] *= 1 + sh / 350; const hw = W / (2 * C[2]), hh = H / (2 * C[2]); C[0] = clamp(C[0], hw, W - hw); C[1] = clamp(C[1], hh, H - hh);
    cam(C, () => fn(z, t), sh, t); ctx.setTransform(1, 0, 0, 1, 0, 0); for (let i = 0; i < HUDQ.length; i++) HUDQ[i](); break; } }
window.render = render; window.DURATION = DURATION;
if (!location.search.includes('render')) { const t0 = performance.now(); (function loop() { render(((performance.now() - t0) / 1000) % DURATION); requestAnimationFrame(loop); })(); }
</script></body></html>
