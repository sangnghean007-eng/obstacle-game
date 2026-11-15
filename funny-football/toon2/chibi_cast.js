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
  // Studied from CC-licensed Wikimedia Commons photos (2018, 2023), proportions only, nothing traced.
  // RONALDO: long narrow face, square jaw + strong chin, defined cheekbones, thick straight brows sitting low over deep-set narrow eyes,
  // long straight nose, wide mouth; hair LOW and tight: faded sides, short top combed up/right with a hard part; light-olive skin; stud earring.
  ronaldo: { skin: '#d9a27c', shade: '#b9825e', head: { R: 108, hair: 'cr7', hairCol: '#16100b', faceW: 0.86, faceH: 1.16, jaw: 0.95, chin: 0.9, chinPoint: 0.2, cheekbones: true,
    eyeSize: 0.8, eyeShape: 'almond', lidBase: 0.1, deepEyes: true, eyeGap: 1.05, browW: 0.12, browLen: 1.15, browY: 0.07, browBase: -0.15, browCol: '#16100b',
    iris: '#4a2c16', nose: 0.2, noseLen: 1.2, mouthW: 1.3, earSize: 1.15, earring: '#e5e7eb' } },
  // MESSI: oval face, medium-length wavy hair swept back over the ears, full thick ginger-brown beard + moustache,
  // heavy low brows, deep intense eyes, longish nose; sleeve tattoo; smaller stockier build.
  messi: { head: { R: 104, hair: 'long', hairCol: '#4a2e1c', beard: true, beardCol: '#8a5230', faceW: 0.94, faceH: 1.08, jaw: 0.5,
    eyeSize: 0.8, eyeShape: 'almond', lidBase: 0.15, deepEyes: true, browW: 0.14, browY: 0.07, browBase: -0.12, browCol: '#3b2416', iris: '#3a2416', nose: 0.4, noseLen: 0.9, mouthW: 0.9 }, tattoo: { arm: 'f', col: '#2b3a55' } },
  // HØJLUND: very light platinum-blond short hair, pale skin, slim young face, light brows.
  hoj: { skin: '#f3d3bd', shade: '#dcb39a', head: { R: 102, hair: 'swept', hairCol: '#eadba8', faceH: 1.1, faceW: 0.92, jaw: 0.6, chin: 0.4, eyeSize: 0.85, eyeShape: 'almond', browW: 0.1, browCol: '#c9b07a', iris: '#5b7fb0', nose: 0.3, noseLen: 0.6 } },
  // Others: medium/low confidence (no reference photo yet).
  d1: { head: { R: 104, hair: 'buzz', hairCol: '#7a5a3a', beard: 'trim', beardCol: '#7a5a3a', jaw: 0.7, eyeSize: 0.85, eyeShape: 'almond', browW: 0.13, lidBase: 0.18, iris: '#4a6fa5' } },
  p1: { skin: '#e8c2a0', shade: '#c99f7d', head: { R: 102, hair: 'fade', hairCol: '#1d1410', beard: 'trim', beardCol: '#1d1410', jaw: 0.7, eyeSize: 0.85, eyeShape: 'almond', browW: 0.16, lidBase: 0.15, iris: '#3a2416' } },
  p2: { skin: '#ecc6a4', shade: '#cfa483', head: { R: 100, hair: 'styled', hairCol: '#22160f', stubble: true, faceH: 1.08, faceW: 0.93, jaw: 0.45, eyeSize: 0.85, eyeShape: 'almond', browW: 0.11, iris: '#3a2416' } },
};
