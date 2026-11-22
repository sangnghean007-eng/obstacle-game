"""finish_caric.py — after cut_heads.py: keep the raw cut in caric_full/, trim the head at the neck (skin rule), flatten colours,
and record the cheek skin colour in cast/skins.js.   python3 cast/finish_caric.py <name> [<name> ...]"""
import os, sys, json, re, numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
def finish(n):
    d = os.path.join(HERE, n, 'caric'); full = os.path.join(HERE, n, 'caric_full'); os.makedirs(full, exist_ok=True); meds = []
    for f in sorted(os.listdir(d)):
        if not f.endswith('.png'): continue
        src = os.path.join(full, f)
        if not os.path.exists(src): Image.open(os.path.join(d, f)).save(src)
        a = np.array(Image.open(src).convert('RGBA')).astype(int); A = a[:, :, 3] > 0; h, w = A.shape; R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        skin = A & (R - B > 35) & (G < R * 0.8) & (B < R * 0.75) & (R > 60); xs = slice(int(w * 0.35), int(w * 0.65)); cut = h
        for y in range(h - 1, int(h * 0.5), -1):
            if skin[y, xs].mean() > 0.7: cut = y + 2; break
        a = a[:cut].astype(np.uint8)
        rgb = Image.fromarray(a[:, :, :3]).filter(ImageFilter.MedianFilter(3)).quantize(colors=40, method=Image.Quantize.MEDIANCUT).convert('RGB')
        Image.fromarray(np.dstack([np.array(rgb), a[:, :, 3]])).save(os.path.join(d, f))
        ck = skin[int(h * 0.45):int(h * 0.6), int(w * 0.3):int(w * 0.7)]; px = a[int(h * 0.45):int(h * 0.6), int(w * 0.3):int(w * 0.7), :3][ck]
        if len(px): meds.append(np.median(px, 0))
    m = np.median(np.array(meds), 0).astype(int); return '#%02x%02x%02x' % tuple(m)
p = os.path.join(HERE, 'skins.js'); cur = json.loads(re.search(r'= (\{.*?\});', open(p).read()).group(1))
for n in sys.argv[1:]: cur[n] = finish(n); print(n, cur[n])
open(p, 'w').write('window.CAST_SKIN = ' + json.dumps(cur) + ';  // median cheek colour of each caricature head — limbs use it so face and hands match\n')
