"""Ep36 THE REBUILD sound: synth western (music.py; new genre in the window, 'new sheriff in town') + own ElevenLabs pieces:
hammer/door/roof (door.wav), wrecking ball + rubble (wreck.wav), ball through glass (glass.wav); Pochettino's real words "You will see. Give me time." (library voice 'Jerry B.', not his voice)."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 29.5; d = Desk(D); m = Mix2(D, ep=36)
def snd(name, a=0, b=None):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768; x = x[:, int(a * SR): int(b * SR) if b else None]
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
song = Song('western', key='E', minor=True, seed=36).form([('intro', 1), ('verse', 2), ('drop', 3), ('break', 2), ('outro', 4)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((9.8, 10.9, 0.35), (20.2, 29.5, 0.45)): env[int(a * SR):int(b * SR)] = g        # tense work order; sad rubble
env = np.convolve(env, np.ones(2000) / 2000, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
n = int(D * SR); d.add('crowd', np.stack([np.convolve(np.random.default_rng(36).standard_normal(n), np.ones(400) / 400, 'same') * 3] * 2), 0, .1)   # wind on the building site
m.whoosh(0.4, .5, .2); [m.thump(0.6 + i * 0.5, .12) for i in range(5)]                                              # Carrick's footsteps out
[m.thump(3.1 + i * 0.35, .15) for i in range(3)]; m.cork(3.9, .2); m.whoosh(4.2, .4, .2); m.spring(4.5, .2)           # arrives, flips the hourglass
d.add('vox', snd('vo_time'), 4.6, 5.0, .2)                                                                            # "You will see. Give me time."
d.add('fx', snd('door', 0.25, 0.6), 6.95, .8); d.add('fx', snd('door', 1.9, 3.4), 7.6, .9, .4)                    # fix 1 → roof slides
d.add('fx', snd('door', 0.25, 0.6), 7.95, .8); d.add('fx', snd('wreck', 0.15, 1.2), 8.5, .5, .4)                  # fix 2 → wall chunk
d.add('fx', snd('door', 0.25, 0.6), 8.95, .8); m.slide_whistle(9.15, False, .7, .25); m.thump(9.6, .4)            # fix 3 → scaffolding
m.timpani(9.8, 70, .3, roll=0.4); m.thump(10.75, .35); m.honk(10.8, .2)                                               # De Ligt brick
m.whoosh(10.5, .4, .25); m.thump(10.95, .5); m.whip(11.1, .45)                                                         # Yoro trips Isak → red
for t0 in (12.2, 13.4): m.whoosh(t0 - 0.5, .5, .35); d.add('fx', snd('glass'), t0 - 0.03, 1.0, .3); m.crowd(t0 + 0.1, 'cheer', 0.8, .2)
m.wahwah(14.2, .25)
for i, t0 in enumerate((16.6, 18.2)):
    m.whoosh(t0 - 0.5, .5, .4); d.add('fx', snd('wreck', 0.15, 2.6), t0 - 0.12, .95, (-1) ** i * .2); m.crowd(t0 + 0.15, 'cheer', 0.8, .18)
m.cork(19.0, .2)
m.whoosh(23.1, .4, .25); d.add('fx', snd('glass', 0, 1.2), 23.57, .7); m.thump(23.6, .4); m.wahwah(24.0, .3)          # brick smashes the hourglass
m.whoosh(25.6, 1.0, .2); m.squeak(28.0, .2)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [7.6, 8.5, 10.95, 12.2, 13.4, 16.6, 18.2, 23.6], .45, .15, .4); d.duck('music', [4.6], .78, 2.0, .3); d.duck('drums', [4.6], .78, 2.0, .3); d.duck('bass', [4.6], .78, 2.0, .3); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
