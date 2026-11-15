// chibi character specs (original caricatures; public signifiers only)
window.CH = {
  traore: { skin: '#7a4a2c', shade: '#5c361f', shoulderW: 150, waistW: 82, torsoH: 175, leg: 120, legW: 52, arm: 190, armW: 62, pecs: true, num: '17', numSize: 70, name: 'TRAORÉ', nameSize: 26, blinkSeed: 0.3,
    head: { R: 118, hair: 'short', hairCol: '#141010', beard: true, beardCol: '#1c1410', jaw: 0.6, iris: '#4a2c16', nose: 0.6, browW: 0.16, mouthW: 1.15 },
    kit: { shirt: '#7a263a', sleeve: '#8fd0f0', cuff: '#7a263a', collar: '#8fd0f0', shorts: '#f4f4f4', sock: '#7a263a', sockShade: '#5c1a2b', sockBand: '#8fd0f0', boot: '#ff7a1a', num: '#ffffff' } },
  cucu: { skin: '#f3c9a6', shade: '#dba582', shoulderW: 72, waistW: 58, torsoH: 135, leg: 110, legW: 34, arm: 135, armW: 30, num: '3', numSize: 52, name: 'CUCURELLA', nameSize: 15, blinkSeed: 1.7,
    head: { R: 104, hair: 'curls', hairCol: '#8b5a2e', stubble: true, iris: '#3f6b2a', nose: 0.3 },
    kit: { shirt: '#034694', sleeve: '#034694', cuff: '#ffffff', collar: '#ffffff', shorts: '#034694', sock: '#ffffff', sockShade: '#d5dbe6', sockBand: '#034694', boot: '#ffffff', num: '#ffffff' } },
  mate1: { skin: '#c98a5e', shade: '#a96d45', shoulderW: 74, waistW: 58, torsoH: 135, leg: 110, legW: 34, arm: 135, armW: 30, num: '6', numSize: 52, blinkSeed: 2.3, head: { R: 100, hair: 'short', hairCol: '#2a1a10', iris: '#4a2c16' }, kit: null },
  mate2: { skin: '#5c3a24', shade: '#432818', shoulderW: 74, waistW: 58, torsoH: 135, leg: 110, legW: 34, arm: 135, armW: 30, num: '8', numSize: 52, blinkSeed: 0.9, head: { R: 100, hair: 'bald', hairCol: '#111', iris: '#3a2416' }, kit: null },
  mate3: { skin: '#f1c7a5', shade: '#d9a583', shoulderW: 74, waistW: 58, torsoH: 135, leg: 110, legW: 34, arm: 135, armW: 30, num: '11', numSize: 48, blinkSeed: 3.1, head: { R: 100, hair: 'spiky', hairCol: '#e0a030', iris: '#3f6b9a' }, kit: null },
  mate4: { skin: '#8d5a3b', shade: '#6e432a', shoulderW: 74, waistW: 58, torsoH: 135, leg: 110, legW: 34, arm: 135, armW: 30, num: '20', numSize: 48, blinkSeed: 1.2, head: { R: 100, hair: 'short', hairCol: '#111', iris: '#3a2416' }, kit: null },
  ronaldo: { skin: '#c98a5e', shade: '#a96d45', shoulderW: 118, waistW: 68, torsoH: 160, leg: 120, legW: 44, arm: 170, armW: 44, pecs: true, num: '7', numSize: 66, name: 'RONALDO', nameSize: 20, blinkSeed: 0.6,
    head: { R: 112, hair: 'quiff', hairCol: '#1a120c', jaw: 0.55, iris: '#4a2c16', nose: 0.4, browW: 0.13 },
    kit: { shirt: '#ffd400', sleeve: '#ffd400', cuff: '#1e3a8a', collar: '#1e3a8a', shorts: '#1e3a8a', sock: '#ffd400', sockShade: '#d4b000', sockBand: '#1e3a8a', boot: '#ffffff', num: '#1e3a8a' } },
  danilo: { skin: '#e2b48e', shade: '#c4906a', shoulderW: 122, waistW: 74, torsoH: 172, leg: 126, legW: 46, arm: 176, armW: 46, num: '', name: 'DANILO', nameSize: 30, blinkSeed: 2.1,
    head: { R: 110, hair: 'bald', hairCol: '#2a1a10', beard: true, beardCol: '#2a1a10', jaw: 0.5, iris: '#3a2416', nose: 0.5, browW: 0.15 },
    kit: { shirt: '#ffd60a', stripes: '#111111', sleeve: '#111111', cuff: '#ffd60a', collar: '#111111', shorts: '#111111', sock: '#111111', sockShade: '#000000', sockBand: '#ffd60a', boot: '#111111', num: '#ffffff' } },
  casemiro: { skin: '#a8724b', shade: '#8a5a38', shoulderW: 116, waistW: 70, torsoH: 160, leg: 118, legW: 44, arm: 168, armW: 44, num: '', numSize: 64, name: '', nameSize: 34, blinkSeed: 0.8,
    head: { R: 110, hair: 'short', hairCol: '#1a120c', beard: true, beardCol: '#1f1510', jaw: 0.6, iris: '#3a2416', nose: 0.5, browW: 0.15 },
    kit: { shirt: '#f5a3c7', sleeve: '#f5a3c7', cuff: '#111', collar: '#111', shorts: '#111111', sock: '#f5a3c7', sockShade: '#d985a3', sockBand: '#111', boot: '#ffffff', num: '#111' } },
  messi: { skin: '#e6b38d', shade: '#c8916b', shoulderW: 92, waistW: 60, torsoH: 140, leg: 108, legW: 36, arm: 140, armW: 32, num: '10', numSize: 56, name: 'MESSI', nameSize: 18, blinkSeed: 2.7,
    head: { R: 104, hair: 'short', hairCol: '#3b2416', beard: true, beardCol: '#5b3a24', jaw: 0.3, iris: '#3a2416', nose: 0.4 },
    kit: { shirt: '#f5a3c7', sleeve: '#f5a3c7', cuff: '#111', collar: '#111', shorts: '#111111', sock: '#f5a3c7', sockShade: '#d985a3', sockBand: '#111', boot: '#ffd21f', num: '#111' } },
  galaxy: { skin: '#f1c7a5', shade: '#d9a583', shoulderW: 100, waistW: 66, torsoH: 150, leg: 116, legW: 40, arm: 160, armW: 38, num: '', name: '', blinkSeed: 1.4,
    head: { R: 104, hair: 'spiky', hairCol: '#c58b3a', iris: '#3f6b9a', nose: 0.5 },
    kit: { shirt: '#ffffff', sleeve: '#0b2c5a', cuff: '#d4a017', collar: '#d4a017', shorts: '#0b2c5a', sock: '#ffffff', sockShade: '#ddd', sockBand: '#d4a017', boot: '#0b2c5a', num: '#0b2c5a' } },
};
for (const k of ['mate1', 'mate2', 'mate3', 'mate4']) window.CH[k].kit = window.CH.cucu.kit;

// ---------- likeness v2 (Nov 15 2026): caricature specs that push each player's most distinctive traits ----------
// Traits come from widely known public appearance (2026). Confidence noted per player; the user reviews the sheet.
window.LIKE = {
  // HIGH confidence: strong angular jaw + pointed chin, high cheekbones, thin arched groomed brows, big white smile,
  // short faded sides with a textured top pushed up, stud earring, clean-shaven, athletic V-shape.
  ronaldo: { head: { R: 112, hair: 'fade', quiff: 1, hairCol: '#1a120c', jaw: 0.8, chin: 0.6, chinPoint: 0.5, cheekbones: true, faceW: 0.94, faceH: 1.06, browArch: 0.2, browW: 0.07, browLen: 1.1, eyeShape: 'almond', eyeSize: 1.0, iris: '#4a2c16', nose: 0.3, mouthW: 1.4, earring: '#e5e7eb' } },
  // HIGH: full trimmed beard (brown, slightly reddish), rounder face, short neat hair, sleeve tattoo on one arm, smaller and stockier build.
  messi: { head: { R: 106, hair: 'sidepart', hairCol: '#3b2416', beard: 'trim', beardCol: '#6b4128', faceW: 1.04, faceH: 0.97, jaw: 0.35, eyeShape: 'almond', lidBase: 0.12, browW: 0.11, iris: '#3a2416', nose: 0.5, mouthW: 0.95 }, tattoo: { arm: 'f', col: '#2b3a55' } },
  // MEDIUM: tall young striker, light brown/blond hair swept back, fair skin, clean-shaven, strong straight brows.
  hoj: { head: { R: 104, hair: 'swept', hairCol: '#b58a4f', faceH: 1.06, faceW: 0.95, jaw: 0.5, chin: 0.3, browW: 0.12, browCol: '#8a6538', iris: '#4a6fa5', nose: 0.4 } },
  // MEDIUM: shaved/buzzed head with a trimmed beard, fair skin, intense look.
  d1: { head: { R: 104, hair: 'buzz', hairCol: '#7a5a3a', beard: 'trim', beardCol: '#7a5a3a', jaw: 0.6, browW: 0.13, lidBase: 0.15, iris: '#4a6fa5' } },
  // MEDIUM: dark short hair, full trimmed beard, light skin, heavy brows (Portugal centre-back).
  p1: { skin: '#e8c2a0', shade: '#c99f7d', head: { R: 102, hair: 'fade', hairCol: '#1d1410', beard: 'trim', beardCol: '#1d1410', jaw: 0.7, browW: 0.16, lidBase: 0.12, iris: '#3a2416' } },
  // MEDIUM: slim young forward with voluminous dark styled hair, light skin, light stubble.
  p2: { skin: '#ecc6a4', shade: '#cfa483', head: { R: 100, hair: 'styled', hairCol: '#22160f', stubble: true, faceH: 1.05, faceW: 0.95, jaw: 0.4, browW: 0.11, iris: '#3a2416' } },
  // LOW (generic but neat): other players keep the base look with a short fade.
};
