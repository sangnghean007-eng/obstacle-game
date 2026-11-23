"""Ep40 PENALTY PODIUM sound — fully synthesized this time (ElevenLabs free credits used up until ~3 Dec):
funk bed (music.py, new seed/key), fx2 hits with fresh seeds, vox2 voices for Mbappé / Yamal / Raphinha (yelps, laughs, hmph)."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 28.5; d = Desk(D); m = Mix2(D, ep=40)
song = Song('funk', key='Bb', minor=False, seed=40).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((4.4, 5.0, 0.25), (8.4, 9.4, 0.25), (24.0, 28.5, 0.55)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
def whistle(t, dur=.35, g=.35):
    k = np.arange(int(dur * SR)) / SR; x = np.sin(2 * np.pi * 2900 * k) * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * k)) * np.minimum(1, k * 40) * np.minimum(1, (dur - k) * 30); m.f(x * g, t, .4)
m.crowd(0.2, 'cheer', 1.5, .2); m.vo('mbappe', 'hmph', 1.4, .5, -.3); m.vo('yamal', 'laugh', 2.2, .4, .3, 'snicker')
whistle(4.1, .4); m.whoosh(4.3, .3, .3); m.thump(4.6, .6); m.whoosh(4.7, 1.2, .45); m.slide_whistle(4.8, True, 1.0, .3); m.crowd(5.2, 'ooh', 1.4, .4)
m.vo('yamal', 'laugh', 5.6, .55, .3, 'belly'); m.vo('mbappe', 'no', 6.0, .5, -.3)
m.whoosh(8.3, .3, .3); m.thump(8.6, .5); m.whip(8.65, .3); m.bonk(9.15, 1.0); m.thump(9.18, .5); m.vo('mbappe', 'ow', 9.25, .6, -.3); m.slide_whistle(9.4, False, .7, .25)
m.crowd(9.6, 'laugh', 1.4, .35); m.vo('mbappe', 'laugh', 10.0, .55, -.3, 'belly'); m.vo('yamal', 'uhoh', 10.2, .5, .3)
[m.thump(11.4 + i * 0.12, .15) for i in range(5)]; m.whip(12.0, .45); m.vo('generic_m', 'hmph', 12.1, .55, .3); m.vo('yamal', 'yelp', 12.2, .5, 0)
m.honk(13.3, .2); whistle(13.6, .25, .25)
m.whoosh(16.0, .4, .2); m.cork(16.2, .3); m.spring(16.35, .25); m.cork(16.5, .3); m.crowd(16.4, 'cheer', 1.6, .3); m.vo('yamal', 'yay', 16.6, .5, .2)
m.vo('generic_m', 'grunt', 15.6, .3, .4); m.vo('generic_m', 'grunt', 16.8, .3, .4); m.vo('generic_m', 'oof', 18.4, .35, .4)   # Atlético tries to climb
[m.thump(20.0 + i * 0.11, .14) for i in range(14)]; m.vo('mbappe', 'yelp', 20.5, .45, -.4); m.vo('yamal', 'yelp', 20.6, .45, .4)
m.whoosh(21.4, .3, .35); m.thump(21.6, .6); m.whoosh(21.7, .5, .35); m.boom(22.1, .5); m.whip(22.1, .5); m.crowd(22.2, 'cheer', 2.0, .45); whistle(22.3, .5, .3)
m.vo('generic_m', 'yay', 22.4, .5, 0); m.vo('mbappe', 'no', 22.6, .45, -.4); m.vo('yamal', 'no', 22.7, .45, .4)
m.vo('mbappe', 'hmph', 24.4, .45, -.3); m.vo('yamal', 'hmph', 24.7, .45, .3)
m.whoosh(25.8, .5, .3); m.bonk(26.3, 1.0); m.slide_whistle(26.4, False, .7, .25); m.vo('mbappe', 'ow', 26.4, .55, -.3); m.vo('yamal', 'laugh', 26.7, .6, .3, 'belly'); m.crowd(26.8, 'laugh', 1.6, .35)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [4.6, 9.15, 22.1, 26.3], .45, .15, .4); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
