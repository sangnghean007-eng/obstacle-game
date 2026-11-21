"""M1b demo: channel sting + a 30 s phonk track with stems, through the new desk."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from music import Song, Inst, mtof, tt, SR
from mix import Desk
out = sys.argv[1]; os.makedirs(out, exist_ok=True)

def sting(rng):  # 2.5 s channel ident: whistle blow → ball thump → 3-note bell "Soc-cer three-six-five" + crowd swell
    I = Inst(rng); d = Desk(2.6)
    t = tt(.35); wh = np.sign(np.sin(2 * np.pi * 2900 * t)) * (1 + .5 * np.sign(np.sin(2 * np.pi * 32 * t))) * np.exp(-t * 4) * .15; d.add('fx', wh, 0)
    d.add('drums', I.kick(.5, 1.4, 45), .42, 1.0); d.add('fx', I.impact(1.6), .42, .5)
    for i, (m, tm) in enumerate(((76, .62), (79, .8), (84, 1.0))): d.add('music', I.bell(m, 1.4), tm, .8, (-.3, 0, .3)[i]); d.add('music', I.piano(m - 12, 1.2), tm, .4, (-.3, 0, .3)[i])
    n = tt(1.8); cr = np.convolve(rng.standard_normal(len(n)), np.ones(40) / 40, 'same') * np.minimum(1, n / .8) * np.exp(-np.maximum(0, n - 1) * 2) * 3
    d.add('crowd', np.stack([cr, np.roll(cr, 400)]), .6, .35); d.room('music', 'stadium', .25); d.room('fx', 'stadium', .2); return d

r = np.random.default_rng(365); d = sting(r); print('sting', d.master(os.path.join(out, 'soccer365-sting.wav')))
s = Song('phonk', key='F#', minor=True, seed=31).form([('intro', 2), ('build', 2), ('drop', 6), ('break', 2), ('drop', 4)])
st = s.render(); L = s.length() + 2; d = Desk(L); d.add_stems(st); d.duck('music', s.kick_times, .3, .02, .12); d.duck('bass', s.kick_times, .5, .01, .1)
d.room('music', 'hall', .15); d.room('fx', 'hall', .2)
print('track', round(L, 1), 's', d.master(os.path.join(out, 'phonk-demo.wav'), os.path.join(out, 'stems')))
