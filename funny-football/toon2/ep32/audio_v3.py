"""Ep32 TRUST FALL sound (engine v2): playful Latin groove (new genre in the window), phone-video room tone, cartoon foley; record-scratch on the realisation; big bonk; kids-style laughter."""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from music import Song, Inst, tt, SR
from mix import Desk
from fx2 import Mix2
D = 16.7; d = Desk(D); I = Inst(np.random.default_rng(32)); m = Mix2(D, ep=32)
song = Song('latin', key='D', minor=False, seed=32).form([('intro', 1), ('verse', 2), ('break', 1), ('drop', 3)]); st = song.render()
L = len(st['drums']); env = np.ones(L); a, b = int(7.0 * SR), int(8.6 * SR); env[a:b] = 0.15; env = np.convolve(env, np.ones(1500) / 1500, 'same')
d.add_stems({k: v[:L] * env for k, v in st.items()})
n = tt(D); d.add('crowd', np.stack([np.convolve(np.random.default_rng(1).standard_normal(len(n)), np.ones(400) / 400, 'same') * 3] * 2), 0, .12)  # outdoor room tone
m.vo('mbappe', 'laugh', .5, .4, -.3, 'snicker')
m.whoosh(3.0, 2.0, .3); m.vo('yamal', 'yelp', 4.3, .5)
m.thump(5.05, .5); m.xylo_rise(5.2, .2); m.vo('yamal', 'laugh', 5.5, .35, .2, 'giggle')
m.f(np.concatenate([np.sin(2 * np.pi * np.cumsum(np.linspace(900, 200, int(.25 * SR))) / SR), np.zeros(10)]) * .6, 7.55, .5)  # record scratch
m.slide_whistle(9.0, False, 1.0, .35); m.bonk(10.2, .9); m.thump(10.22, .8); m.vo('yamal', 'oof', 10.25, .6)
for i, w in enumerate(('kid', 'generic_m', 'kid', 'generic_f')): m.vo(w, 'laugh', 10.6 + i * .12, .45, -.6 + i * .4, ['belly', 'point', 'giggle', 'cackle'][i])
m.spring(11.2, .3); m.vo('mbappe', 'laugh', 11.5, .4, -.3, 'point')
m.vo('yamal', 'hmph', 13.6, .45); m.whoosh(14.6, .9, .3); m.bonk(15.5, .9); m.thump(15.52, .8); m.vo('mbappe', 'ow', 15.55, .55)
for i, w in enumerate(('kid', 'generic_m', 'yamal')): m.vo(w, 'laugh', 15.8 + i * .1, .45, -.5 + i * .5, ['point', 'belly', 'cackle'][i])
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0); d.duck('music', [7.55, 10.2, 15.5], .5, .2, .5); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release', 'stems')))
