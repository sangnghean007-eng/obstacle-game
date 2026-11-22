"""Ep39 BLOCK BY BLOCK: MESSI sound: synth latin (music.py) + own ElevenLabs pieces (calm block click, trophy tower rising);
character signatures carried over as running gags: Ronaldo's SIUUU (Ep35 take), Messi's mate slurp (Ep37 take)."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 28.0; d = Desk(D); m = Mix2(D, ep=39)
def snd(name, a=0, b=None):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768; x = x[:, int(a * SR): int(b * SR) if b else None]
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
song = Song('latin', key='A', minor=True, seed=39).form([('intro', 2), ('verse', 3), ('drop', 4), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((3.3, 5.0, 0.3), (19.8, 22.4, 0.4)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
d.add('fx', snd('place'), 0.85, .9); d.add('fx', snd('slurp_messi', 0, 1.2), 1.6, .8, -.2)
d.add('vox', snd('siu_cr7'), 3.3, 2.0, .4); m.whoosh(7.0, 1.2, .2)
[d.add('fx', snd('place', 0, .35), 11.1 + i * 0.093, .35, (i % 2) * .4 - .2) for i in range(30)]   # 30 goals in 2026, rapid
d.add('fx', snd('tower'), 15.0, 1.0); d.add('fx', snd('tower', 1.5), 17.2, .6); m.crowd(18.3, 'ooh', 1.4, .35)
d.add('fx', snd('slurp_messi', 0, 1.2), 18.3, .7, -.2)
m.whoosh(19.8, .4, .3); m.thump(20.35, .6); m.honk(20.5, .2); m.whoosh(22.2, .3, .3); m.bonk(22.3, .5); m.slide_whistle(22.4, False, .7, .25)
d.add('fx', snd('slurp_messi', 0, 1.2), 22.7, .7, -.2)
d.add('fx', snd('place'), 24.2, .6); m.crowd(25.0, 'laugh', 1.2, .25)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [0.85, 15.0, 20.35], .45, .2, .4); d.duck('music', [3.3], .6, 1.6, .3); d.duck('drums', [3.3], .6, 1.6, .3); d.duck('bass', [3.3], .6, 1.6, .3); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
