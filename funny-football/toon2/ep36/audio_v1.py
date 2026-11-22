"""Ep36 THE REBUILD sound: synth western (music.py; new genre in the window, 'new sheriff in town') + own ElevenLabs pieces:
hammer/door/roof (door.wav), wrecking ball + rubble (wreck.wav); Pochettino's real words "You will see. Give me time." (library voice 'Jerry B.', not his voice)."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 27.0; d = Desk(D); m = Mix2(D, ep=36)
def snd(name, a=0, b=None):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768; x = x[:, int(a * SR): int(b * SR) if b else None]
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
song = Song('western', key='E', minor=True, seed=36).form([('intro', 1), ('verse', 2), ('drop', 3), ('break', 2), ('outro', 3)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((12.8, 15.6, 0.3), (20.8, 27.0, 0.45)): env[int(a * SR):int(b * SR)] = g        # tense work order; sad rubble
env = np.convolve(env, np.ones(2000) / 2000, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
n = int(D * SR); d.add('crowd', np.stack([np.convolve(np.random.default_rng(36).standard_normal(n), np.ones(400) / 400, 'same') * 3] * 2), 0, .1)   # wind on the building site
m.whoosh(0.4, .5, .2); [m.thump(0.6 + i * 0.55, .12) for i in range(6)]                                              # Carrick's footsteps out
[m.thump(3.6 + i * 0.4, .15) for i in range(4)]; m.cork(4.3, .2)                                                       # Pochettino arrives, sets the toolbox down
d.add('vox', snd('vo_time'), 4.6, 5.0, .2)                                                                            # "You will see. Give me time."
d.add('fx', snd('door', 0.25, 0.6), 7.95, .9); d.add('fx', snd('door', 1.75, 2.5), 8.45, 1.0); m.slide_whistle(8.6, False, .7, .2)
m.spring(9.6, .25); d.add('fx', snd('door', 1.9, 3.4), 10.7, .9, .4); m.whoosh(10.0, .7, .3)
d.add('fx', snd('door', 0.25, 0.6), 11.15, .8); d.add('fx', snd('wreck', 0.15, 1.4), 12.05, .55, .4); m.wahwah(12.3, .22)
m.timpani(13.0, 60, .35, roll=1.4); m.whoosh(14.0, .9, .3)
m.whoosh(15.85, .4, .25); m.honk(16.3, .25)                                                                            # Yoro's red brick
for i, t0 in enumerate((16.6, 17.6, 18.6, 19.6)):
    m.whoosh(t0 - 0.5, .5, .4); d.add('fx', snd('wreck', 0.15 + (i % 2) * 0.1, 2.6 if i in (0, 3) else 1.3), t0 - 0.12, .95 if i in (0, 3) else .75, (-1) ** i * .2)
    m.crowd(t0 + 0.15, 'cheer', 0.8, .18)                                                                             # the away end (Anfield)
m.wahwah(21.0, .3); m.bonk(24.4, .8); m.slide_whistle(24.55, False, .6, .2); m.squeak(25.2, .2)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [8.45, 10.7, 12.05, 16.6, 17.6, 18.6, 19.6], .45, .15, .4); d.duck('music', [4.6], .78, 2.0, .3); d.duck('drums', [4.6], .78, 2.0, .3); d.duck('bass', [4.6], .78, 2.0, .3); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
