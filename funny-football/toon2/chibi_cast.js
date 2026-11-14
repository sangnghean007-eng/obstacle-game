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
};
for (const k of ['mate1', 'mate2', 'mate3', 'mate4']) window.CH[k].kit = window.CH.cucu.kit;
