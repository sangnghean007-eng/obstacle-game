"""Ep33 GENERAL MBAPPÉ sound: orchestral march (new in the 6-episode window), a slap per Real goal (26, every one different),
crowd 'oooh' builds, record scratch on PENALTY MISSED, the revenge slap, slide-whistle exit for PSV. Timings = scene.html."""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from music import Song, tt, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 23.1; d = Desk(D); m = Mix2(D, ep=33)
song = Song('orchestral', key='C', minor=False, seed=33).form([('intro', 1), ('verse', 2), ('drop', 3), ('break', 1), ('outro', 1)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L); a, b = int(16.85 * SR), int(17.9 * SR); env[a:b] = 0.12; env = np.convolve(env, np.ones(1200) / 1200, 'same')
d.add_stems({k: v[:L] * env for k, v in st.items()})
n = tt(D); d.add('crowd', np.stack([np.convolve(np.random.default_rng(3).standard_normal(len(n)), np.ones(300) / 300, 'same') * 4] * 2), 0, .14)
m.timpani(0.0, 90, .6, roll=1.2); m.timpani(2.5, 70, .5)
SL = [3.3, 5.0, 5.45, 5.9, 6.35, 7.45, 7.75, 8.05, 8.35, 9.05, 9.3, 9.55, 9.8, 11.0, 12.1, 13.6, 13.75, 13.9, 14.0, 14.15, 14.3, 14.4, 14.55, 14.7, 15.9, 16.4]
for i, s in enumerate(SL): m.whip(s - 0.06, .25, .2); m.smack(s, .75 if s != 12.1 else .95, -.2 + (i % 3) * .2)
for s in (3.5, 6.6, 8.6, 10.0, 12.4, 15.0, 16.6): m.crowd(s, 'ooh', 1.0, .25)
m.slide_whistle(11.6, False, .5, .25); m.boom(12.1, .5)                              # Clásico slow-mo slap
m.f(np.concatenate([np.sin(2 * np.pi * np.cumsum(np.linspace(900, 200, int(.25 * SR))) / SR), np.zeros(10)]) * .6, 16.85, .5)  # PENALTY MISSED
m.vo('mbappe', 'hmph', 17.2, .4); m.whip(17.76, .3); m.smack(17.82, 1.0, .2); m.vo('mbappe', 'ow', 17.9, .55); m.spring(18.1, .3)
m.crowd(18.0, 'laugh', 1.6, .35); m.slide_whistle(20.6, True, .8, .35); m.vo('mbappe', 'laugh', 21.6, .35, -.2, 'giggle')
_sr, sting = wavfile.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx', 'demo', 'soccer365-sting.wav')); sting = sting.astype(float) / (32768 if sting.dtype == np.int16 else 1)
sting = (sting.T if sting.ndim == 2 else np.stack([sting] * 2)); d.add('fx', sting[:, :int((D - 21.2) * SR)], 21.2, .5)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0); d.duck('music', SL + [17.82], .25, .1, .2); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release', 'stems')))
