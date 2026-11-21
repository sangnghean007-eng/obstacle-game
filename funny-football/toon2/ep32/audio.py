"""Ep32 TRUST FALL v4 sound (engine v2): Latin groove that stops dead on '…next GOAT?', cartoon foley on every catch,
a long slide-whistle fall, a big bonk + face-plant crunch, then the groove back with laughter. Timings = scene.html v4."""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from music import Song, Inst, tt, SR
from mix import Desk
from fx2 import Mix2
D = 20.1; d = Desk(D); m = Mix2(D, ep=32)
song = Song('latin', key='D', minor=False, seed=320).form([('intro', 1), ('verse', 2), ('break', 1), ('drop', 3), ('outro', 1)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
a, b = int(10.15 * SR), int(13.0 * SR); env[a:b] = 0.12                    # music drops out for the 'next GOAT?' stare and the fall
env = np.convolve(env, np.ones(1200) / 1200, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
n = tt(D); d.add('crowd', np.stack([np.convolve(np.random.default_rng(1).standard_normal(len(n)), np.ones(400) / 400, 'same') * 3] * 2), 0, .12)  # park air
# 1 Messi: tip, caught
m.whoosh(0.0, .45, .25); m.thump(0.4, .55); m.xylo_rise(0.5, .2); m.vo('messi', 'laugh', 0.9, .3, .2, 'giggle')
for i, w in enumerate(('kid', 'generic_f')): m.vo(w, 'laugh', 1.3 + i * .15, .3, .5, ['giggle', 'point'][i])
m.whoosh(1.95, .5, .15)                                                    # pushed back up
# 2-3 Mbappé
m.vo('mbappe', 'yelp', 3.5, .5, .3); m.spring(3.7, .25); m.spring(4.1, .2)
m.whoosh(5.3, .75, .3); m.vo('mbappe', 'yelp', 5.6, .45, .3); m.thump(6.05, .7); m.vo('ronaldo', 'oof', 6.1, .5, -.3); m.xylo_rise(6.2, .2)
m.vo('mbappe', 'laugh', 6.6, .4, .3, 'belly'); m.whoosh(7.2, .5, .15)
# 4-5 Yamal brags, Ronaldo stares
m.vo('yamal', 'yelp', 8.1, .5, 0); m.spring(8.6, .25); m.vo('yamal', 'laugh', 8.9, .35, 0, 'giggle')
m.f(np.concatenate([np.sin(2 * np.pi * np.cumsum(np.linspace(900, 200, int(.25 * SR))) / SR), np.zeros(10)]) * .6, 10.15, .5)  # record scratch
m.vo('ronaldo', 'hmph', 10.5, .45)
# 6 the fall nobody catches
m.slide_whistle(11.2, False, 1.6, .4); m.whoosh(11.55, .35, .3)         # Ronaldo steps back
m.vo('yamal', 'yelp', 12.0, .5); m.bonk(12.9, .95); m.thump(12.92, .9); m.vo('yamal', 'oof', 12.95, .6)
for i, w in enumerate(('kid', 'generic_m', 'mbappe', 'generic_f')): m.vo(w, 'laugh', 13.1 + i * .12, .45, -.6 + i * .4, ['belly', 'point', 'cackle', 'giggle'][i])
# 7 face in the grass
m.thump(13.8, .6); m.spring(14.3, .2); m.vo('yamal', 'ow', 14.6, .5)
# 8 GOATs only
m.xylo_rise(16.1, .3); m.vo('messi', 'laugh', 17.8, .35, .2, 'giggle'); m.vo('ronaldo', 'laugh', 17.9, .4, -.2, 'belly')
for i, w in enumerate(('kid', 'generic_m')): m.vo(w, 'laugh', 18.2 + i * .15, .35, -.4 + i * .8, ['point', 'cackle'][i])
from scipy.io import wavfile                                                # channel sting closes every episode
_sr, sting = wavfile.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx', 'demo', 'soccer365-sting.wav')); sting = sting.astype(float) / (32768 if sting.dtype == np.int16 else 1)
sting = (sting.T if sting.ndim == 2 else np.stack([sting] * 2)); d.add('fx', sting[:, :int((D - 18.2) * SR)], 18.2, .5)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0); d.duck('music', [0.4, 6.05, 12.9], .5, .2, .5); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release', 'stems')))
