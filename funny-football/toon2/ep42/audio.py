"""Ep42 THE CHASE sound — fully synthesized. Surf-rock chase bed; scooter engine drone, VROOM + soot cough, leap whoosh + faceplant,
fishing-rod reel/zip per lunge, tyre skid at the road sign, honks, cries, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 24.4; d = Desk(D); m = Mix2(D, ep=42)
song = Song('surf', key='A', minor=True, seed=42).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((16.5, 19.5, 0.35), (19.5, D, 0.7)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(42)
def tt(dur): return np.arange(int(dur * SR)) / SR
def engine(t0, t1, g=.12, f0=62):
    k = tt(t1 - t0); f = f0 * (1 + .05 * np.sin(2 * np.pi * .7 * k)); x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * k)); x = np.convolve(x, np.ones(40) / 40, 'same'); m.f(x * g, t0, .3)
def vroom(t, g=.5):
    k = tt(1.0); f = 60 + 200 * np.minimum(1, k * 3) * np.exp(-k * 1.5); x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)); x = np.convolve(x, np.ones(30) / 30, 'same') * np.exp(-k * 1.8); m.f(x * g, t, .3)
def skid(t, g=.4):
    k = tt(.9); x = np.sin(2 * np.pi * np.cumsum(2200 + 400 * np.sin(2 * np.pi * 13 * k)) / SR) * r.standard_normal(len(k)) * .5 * np.exp(-k * 2); m.f(x * g, t, 0)
engine(0.0, 16.9, .1); engine(19.5, D, .05, 70)
m.crowd(0.2, 'cheer', 1.2, .15); m.honk(0.6, .25); m.honk(0.85, .25); m.vo('generic_m', 'laugh', 1.2, .45, .3, 'snicker')
[m.thump(2.6 + i * .14, .12) for i in range(18)]; m.vo('mbappe', 'gasp', 2.9, .5, -.3); m.slide_whistle(3.6, True, .5, .18)
m.vo('generic_m', 'laugh', 5.6, .5, .3, 'belly'); m.whoosh(6.0, .5, .3); m.vo('mbappe', 'yelp', 6.7, .45, -.2)
vroom(7.2, .55); m.whoosh(7.25, .6, .4); m.vo('mbappe', 'oof', 7.6, .55, -.2); [m.vo('mbappe', 'grunt', 8.0 + i * .25, .3, -.2) for i in range(2)]; m.vo('generic_m', 'laugh', 7.8, .45, .3, 'snicker')
m.whoosh(9.55, .8, .45); m.slide_whistle(9.6, True, .6, .28); m.vo('mbappe', 'yelp', 9.7, .5, -.1); m.slide_whistle(10.2, False, .4, .28); m.thump(10.6, .8); m.smack(10.62, .6); [m.thump(10.7 + i * .08, .15) for i in range(6)]; m.vo('mbappe', 'cry', 10.9, .5, -.2)
for a in (12.8, 13.8, 14.8): m.vo('mbappe', 'grunt', a, .45, -.2); m.zip(a + .1, .3); m.spring(a + .15, .25)
m.vo('generic_m', 'laugh', 13.3, .45, .3, 'snicker'); m.xylo(12.2, ['E5', 'G5', 'E5'], .12, .12)
skid(16.55, .45); m.record_scratch(16.6, .35); m.sub_boom(17.0, .45); m.vo('mbappe', 'gasp', 17.1, .55, -.1); m.fail_horn(18.0, .18); m.vo('mbappe', 'no', 18.6, .55, -.1)
m.honk(19.8, .2); m.honk(20.05, .2); m.vo('mbappe', 'cry', 20.2, .65, -.2, 'wail'); m.vo('generic_m', 'laugh', 20.6, .3, .5, 'snicker')
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [7.2, 10.6, 16.6, 17.0], .45, .15, .4); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
