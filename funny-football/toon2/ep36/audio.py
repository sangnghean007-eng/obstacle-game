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
for a, b, g in ((9.6, 10.8, 0.35), (20.2, 25.6, 0.45)): env[int(a * SR):int(b * SR)] = g        # tense work order; sad rubble
env = np.convolve(env, np.ones(2000) / 2000, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
n = int(D * SR); d.add('crowd', np.stack([np.convolve(np.random.default_rng(36).standard_normal(n), np.ones(400) / 400, 'same') * 3] * 2), 0, .1)   # wind on the building site
def whistle(t, dur=.35, g=.35):
    k = np.arange(int(dur * SR)) / SR; x = np.sin(2 * np.pi * 2900 * k) * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * k)) * np.minimum(1, k * 40) * np.minimum(1, (dur - k) * 30); m.f(x * g, t, .4)
m.whoosh(0.4, .5, .2); [m.thump(0.6 + i * 0.5, .12) for i in range(5)]; m.vo('generic_m', 'hmph', 1.6, .3, .3)               # Carrick out, crew grumbles
[m.thump(2.0 + i * 0.35, .15) for i in range(3)]; m.cork(2.9, .2); m.whoosh(3.6, .4, .2); m.spring(3.95, .2)            # Pochettino arrives, flips the hourglass
d.add('vox', snd('vo_time'), 4.0, 5.0, .2)                                                                            # "You will see. Give me time."
[m.spring(4.7 + i * 0.08, .12) for i in range(5)]                                                                     # five mini hourglasses flipped
m.vo('generic_m', 'yelp', 6.6, .35, -.4); m.whoosh(7.3, .7, .35); m.bonk(7.55, .7); m.bonk(7.8, .7, ); m.slide_whistle(7.9, False, .6, .2)
d.add('fx', snd('door', 1.9, 3.4), 8.3, .8, -.3); d.add('fx', snd('wreck', 0.15, 1.2), 9.0, .5, .4)                 # scaffolding, roof, wall go
m.timpani(9.6, 70, .3, roll=0.4); m.thump(10.35, .4); m.honk(10.4, .2)                                                # De Ligt drops the plank
m.whoosh(10.45, .4, .25); m.thump(10.9, .5); whistle(11.0, .6, .45); m.whip(11.2, .45); m.vo('generic_m', 'yelp', 11.5, .4, .2)   # Yoro trips Isak, whistle, red
for t0 in (12.4, 13.6): m.whoosh(t0 - 0.5, .5, .35); d.add('fx', snd('glass'), t0 - 0.03, 1.0, .3); m.crowd(t0 + 0.1, 'laugh', 1.0, .3)
m.wahwah(14.3, .25)
for i, t0 in enumerate((16.6, 18.2)):
    m.whoosh(t0 - 0.5, .5, .4); d.add('fx', snd('wreck', 0.15, 2.6), t0 - 0.12, .95, (-1) ** i * .2); m.crowd(t0 + 0.15, 'cheer', 0.8, .2)
[m.thump(15.8 + i * 0.25, .12) for i in range(12)]; m.cork(19.0, .2)                                                    # MU crew scatters
whistle(20.6, .3, .3); m.vo('generic_m', 'hmph', 21.0, .35, .4)
m.whoosh(23.1, .4, .25); d.add('fx', snd('glass', 0, 1.2), 23.57, .7); m.thump(23.6, .4); m.wahwah(24.0, .3)
m.crowd(25.8, 'laugh', 1.4, .3); [m.cork(26.3 + i * 0.95, .25) for i in range(3)]; m.squeak(28.6, .2)                 # selfie clicks
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [7.55, 8.3, 10.9, 12.4, 13.6, 16.6, 18.2, 23.6], .45, .15, .4); d.duck('music', [4.0], .78, 2.0, .3); d.duck('drums', [4.0], .78, 2.0, .3); d.duck('bass', [4.0], .78, 2.0, .3); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
