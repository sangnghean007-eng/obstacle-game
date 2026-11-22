"""Ep34 THE THROW-IN sound: trailer-style drama (new genre in the window), stadium crowd, whistle, BONK, three bounces,
card swishes, timpani roll for the Force-O-Meter, a deflating 'pfft' for 'negligible', sad trombone at FT, training-ground echo."""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from music import Song, tt, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 21.1; d = Desk(D); m = Mix2(D, ep=34)
song = Song('trailer', key='D', minor=True, seed=34).form([('intro', 1), ('verse', 1), ('drop', 2), ('break', 1), ('outro', 1)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b in ((4.55, 5.6), (11.8, 13.1), (14.2, 15.2)): env[int(a * SR):int(b * SR)] = 0.15
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
n = tt(D); d.add('crowd', np.stack([np.convolve(np.random.default_rng(4).standard_normal(len(n)), np.ones(260) / 260, 'same') * 4] * 2), 0, .16)
def whistle(t, dur=.35, g=.35):
    k = np.arange(int(dur * SR)) / SR; x = np.sin(2 * np.pi * 2900 * k) * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * k)) * np.minimum(1, k * 40) * np.minimum(1, (dur - k) * 30); m.f(x * g, t, .6)
m.crowd(0.3, 'ooh', 1.2, .15); m.vo('messi', 'hmph', 3.3, .4)
m.whoosh(4.35, .3, .35); m.bonk(4.62, 1.0); m.thump(4.64, .7); m.crowd(4.7, 'ooh', 1.6, .4)
m.slide_whistle(4.8, True, .8, .3); [m.spring(t0, .3) for t0 in (5.62, 6.02, 6.32)]; m.squeak(6.6, .3); m.crowd(6.4, 'laugh', 1.4, .25)
m.vo('messi', 'laugh', 7.0, .3, -.2, 'snicker'); whistle(8.2, .5); m.whoosh(8.0, .6, .2)
m.whip(8.8, .4); m.crowd(8.9, 'ooh', 1.0, .25); m.whip(10.2, .4); m.crowd(10.3, 'laugh', 1.0, .25)
m.honk(11.3, .3); m.timpani(11.8, 80, .5, roll=1.1); m.spring(13.0, .35); m.cork(13.05, .3); m.crowd(13.2, 'laugh', 1.0, .3)
whistle(14.2, .25); whistle(14.5, .25); whistle(14.8, .7); m.wahwah(15.0, .3); m.crowd(15.2, 'cheer', 1.8, .3)
m.whoosh(17.05, .3, .3); m.whoosh(18.35, .3, .3); m.bonk(18.65, .9); m.thump(18.9, .6); m.vo('messi', 'laugh', 19.0, .35, 0, 'giggle')
_sr, sting = wavfile.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx', 'demo', 'soccer365-sting.wav')); sting = sting.astype(float) / (32768 if sting.dtype == np.int16 else 1)
sting = (sting.T if sting.ndim == 2 else np.stack([sting] * 2)); d.add('fx', sting[:, :int((D - 19.4) * SR)], 19.4, .5)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0); d.duck('music', [4.62, 8.8, 10.2, 18.65], .4, .15, .4); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release', 'stems')))
