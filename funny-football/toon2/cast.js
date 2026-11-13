// Supporting cast for toon2 (generic, fictional people). Use: CAST.tourist, etc.; draw with toon2.draw(ctx, CAST.x, pose, expr, x, y, s)
(function () {
  const sk = [['#f1c7a5', '#d9a583'], ['#c98a5e', '#a96d45'], ['#8d5a3b', '#6e432a'], ['#5c3a24', '#432818'], ['#e8b796', '#cc9877']];
  const P = (o) => o;
  window.CAST = {
    gk: P({ skin: sk[0][0], shade: sk[0][1], shoulder: 104, waist: 64, leg: 310, arm: 290, num: '1', head: { face: 'square', hair: 'spiky', hairCol: '#e0a030', beard: 'stubble', nose: 1.3 },
      kit: { shirt: '#ff7a00', collar: '#111', shorts: '#111', sock: '#ff7a00', sockShade: '#cc6200', boot: '#111', num: '#111', gloves: '#2bd46a' } }),
    tourist: P({ skin: sk[4][0], shade: sk[4][1], shoulder: 110, waist: 80, leg: 250, arm: 260, head: { face: 'round', wide: 1.12, hair: 'bald', hairCol: '#b07a50', beard: 'mustache', glasses: 'sun', nose: 1.5 },
      kit: { shirt: '#3fb6e8', pattern: 'hawaii', collar: '#3fb6e8', shorts: '#f4a261', sock: sk[4][0], sockShade: sk[4][1], boot: '#e76f51', belly: 1.6 } }),
    auntie: P({ skin: sk[2][0], shade: sk[2][1], shoulder: 92, waist: 66, leg: 270, arm: 250, head: { face: 'round', hair: 'sunhat', hairCol: '#1a1010', capCol: '#ffe8a3', band: '#e63946', lips: '#c2185b', earring: true, nose: 1.1 },
      kit: { shirt: '#ff6fae', collar: '#ff6fae', shorts: '#ff6fae', sock: sk[2][0], sockShade: sk[2][1], boot: '#ffd60a' } }),
    kid: P({ skin: sk[1][0], shade: sk[1][1], shoulder: 70, waist: 46, leg: 190, arm: 180, head: { face: 'round', hair: 'cap', capCol: '#e63946', nose: 0.8, scale: 1.45 },
      kit: { shirt: '#75aadb', stripes: '#ffffff', collar: '#1b2a4a', shorts: '#1b2a4a', sock: '#ffffff', sockShade: '#cfd8e3', boot: '#ffd21f', num: '#1b2a4a' }, num: '10' }),
    presenter: P({ skin: sk[3][0], shade: sk[3][1], shoulder: 104, waist: 62, leg: 300, arm: 280, head: { face: 'long', hair: 'short', hairCol: '#111', beard: 'stubble', nose: 1.2 },
      kit: { shirt: '#1f2937', collar: '#1f2937', shorts: '#1f2937', sock: '#1f2937', sockShade: '#111', boot: '#111', tie: '#d4a017', lapel: '#ffffff' } }),
    fanCry: P({ skin: sk[0][0], shade: sk[0][1], shoulder: 96, waist: 62, leg: 280, arm: 260, head: { face: 'long', hair: 'long', hairCol: '#c58b3a', nose: 1, lips: '#b5485d' },
      kit: { shirt: '#75aadb', stripes: '#ffffff', collar: '#1b2a4a', shorts: '#1b2a4a', sock: '#fff', sockShade: '#cfd8e3', boot: '#fff', num: '#1b2a4a' }, num: '10' }),
    fanAfro: P({ skin: sk[3][0], shade: sk[3][1], shoulder: 100, waist: 64, leg: 290, arm: 270, head: { face: 'square', hair: 'afro', hairCol: '#1a1010', beard: 'full', nose: 1.2 },
      kit: { shirt: '#ffffff', stripes: '#75aadb', collar: '#1b2a4a', shorts: '#1b2a4a', sock: '#fff', sockShade: '#cfd8e3', boot: '#fff', num: '#1b2a4a' } }),
    grandpa: P({ skin: sk[4][0], shade: sk[4][1], shoulder: 88, waist: 60, leg: 260, arm: 250, head: { face: 'long', hair: 'bald', hairCol: '#f2f2f2', beard: 'mustache', glasses: 'round', nose: 1.6 },
      kit: { shirt: '#f1faee', collar: '#a8dadc', shorts: '#457b9d', sock: '#fff', sockShade: '#ddd', boot: '#6d4c41' } }),
  };
})();
