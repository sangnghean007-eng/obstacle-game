// mu_lfc_likeness.js — code-drawn likeness specs (owner 22 Nov: "Vẽ bằng code cho giống"). Most distinctive trait first.
// Checked against free Commons photos where available (De Ligt, Mbeumo); others from widely known appearance (confidence noted).
window.LIKE2 = {
  // FERNANDES (med): long face, pointed chin, wavy dark-brown top swept up, short sides, heavy arched brows, stubble, olive skin
  bruno: { skin: '#d9a27c', shade: '#b9825e', head: { R: 100, hair: 'fade', quiff: 0.5, hairCol: '#3a2616', stubble: true, faceH: 1.14, faceW: 0.9, jaw: 0.5, chin: 0.6, chinPoint: 0.3, browW: 0.16, browArch: 0.5, browCol: '#2a1a10', eyeShape: 'almond', lidBase: 0.12, nose: 0.35, noseLen: 1.15, mouthW: 1.1, iris: '#3a2416' } },
  // DE LIGT (high, photo): blond hair swept up/sideways, broad square face, ginger stubble, fair skin, blue eyes, big frame
  deligt: { skin: '#f1c7a5', shade: '#d9a583', shoulderW: 88, torsoH: 145, head: { R: 104, hair: 'fade', quiff: 0.8, hairCol: '#d9b86a', fadeCol: 'rgba(160,120,60,.35)', stubble: true, faceW: 1.04, faceH: 1.02, jaw: 0.95, chin: 0.8, browW: 0.11, browCol: '#b8945a', iris: '#5b7fb0', nose: 0.35, mouthW: 1.0 } },
  // YORO (med): young, slim long face, short twists on top, dark skin, tall
  yoro: { skin: '#5a3822', shade: '#432818', leg: 122, head: { R: 98, hair: 'twists', hairCol: '#111', faceH: 1.12, faceW: 0.88, jaw: 0.35, chin: 0.45, browW: 0.11, browCol: '#111', iris: '#2a1a10', mouthW: 0.95 } },
  // MAINOO (med): young round face, short twists, thin moustache, dark-brown skin
  mainoo: { skin: '#6e432a', shade: '#55331f', head: { R: 98, hair: 'twists', hairCol: '#111', twistH: -0.04, faceH: 1.02, jaw: 0.4, browW: 0.11, browCol: '#111', iris: '#2a1a10' } },
  // MBEUMO (high, photo): full thick black beard, short hair, medium-brown skin, wide face
  mbeumo: { skin: '#7a4a2e', shade: '#5e3822', head: { R: 100, hair: 'buzz', hairCol: '#111', beard: true, beardCol: '#111', faceW: 1.0, jaw: 0.7, browW: 0.15, browCol: '#111', iris: '#2a1a10' } },
  // ISAK (med-high): very tall & thin, long face, long black hair tied in a bun, light goatee
  isak: { skin: '#7a4a2e', shade: '#5e3822', leg: 128, shoulderW: 68, head: { R: 98, hair: 'bun', hairCol: '#111', stubble: true, faceH: 1.2, faceW: 0.86, jaw: 0.4, chin: 0.65, chinPoint: 0.3, browW: 0.12, browCol: '#111', iris: '#2a1a10' } },
  // SZOBOSZLAI (med-high): blond hair slicked straight back, strong square jaw, high cheekbones, blue eyes, fair skin
  szob: { skin: '#f1c7a5', shade: '#d9a583', head: { R: 102, hair: 'swept', hairCol: '#e8cf8a', faceH: 1.08, jaw: 0.95, chin: 0.9, cheekbones: true, deepEyes: true, browW: 0.12, browCol: '#c9a75a', iris: '#4a6fa5', nose: 0.3 } },
  // WIRTZ (med): boyish round face, short light-brown hair with a fringe, fair skin, big grin
  wirtz: { skin: '#f3cbb0', shade: '#d9a98d', head: { R: 102, hair: 'short', hairCol: '#7a5230', faceW: 0.98, faceH: 1.0, jaw: 0.3, chin: 0.35, browW: 0.1, browCol: '#6a4422', iris: '#5a7a5a', earSize: 1.12, mouthW: 1.1 } },
  // NGUMOHA (med): 17, small, very young round face, twists
  ngumoha: { skin: '#5a3822', shade: '#432818', leg: 100, head: { R: 98, hair: 'twists', hairCol: '#111', twistH: 0.02, faceH: 0.98, jaw: 0.3, browW: 0.1, browCol: '#111', iris: '#2a1a10' } },
  // MUÑOZ (low): dark short hair, trimmed beard, light-olive skin
  munoz: { skin: '#d9a27c', shade: '#b9825e', head: { R: 100, hair: 'fade', hairCol: '#2a1a10', beard: 'trim', beardCol: '#2a1a10', jaw: 0.6, browW: 0.14, browCol: '#2a1a10', iris: '#3a2416' } },
};
