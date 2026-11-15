// Render a portrait at identity scale (design box 600x620) on a transparent canvas.
// Usage: node overlay.js <name> <out.png> [expr|mouth]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => { const [name, out, ex] = process.argv.slice(2); const dir = path.resolve(__dirname, '../../toon2'), f = path.join(dir, '_ov.html');
  const opt = ['siuuu', 'shock', 'smug', 'angry', 'deadpan'].includes(ex) ? `{expr:'${ex}'}` : `{mouth:'${ex || ''}'}`;
  fs.writeFileSync(f, `<html><body style="margin:0;background:transparent"><canvas id=c width=600 height=620></canvas><script src="portrait.js"></script><script>portrait.draw(document.getElementById('c').getContext('2d'),'${name}',330,300,1,${opt});</script></body></html>`);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 600, height: 620 } }); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + f); await p.waitForTimeout(200); await p.locator('#c').screenshot({ path: out, omitBackground: true }); await b.close(); fs.unlinkSync(f); })();
