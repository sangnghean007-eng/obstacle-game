"""Ep45 DEBT COLLECTORS sound — fully synthesized. Western stand-off bed (new seed/key), crutch taps + boots for the march,
the shield's 'CLANG' entrance, ball rebounds (BOINK x2), Adeyemi's rocket whoosh + BONK, Jesus BOING, crutch CLANG on his own ankle, bowling STRIKE, sobbing walk home, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 27.8; d = Desk(D); m = Mix2(D, ep=45)
song = Song('western', key='D', minor=True, seed=45).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((6.4, 7.4, 0.25), (15.1, 15.9, 0.25), (17.8, 18.6, 0.3)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(45)
def tt(dur): return np.arange(int(dur * SR)) / SR
def tap(t, g=.25): k = tt(.06); m.f(np.sin(2 * np.pi * 900 * k) * np.exp(-k * 80) * g, t, -.3)
def strike(t, g=.6):  # bowling: rolling rumble then pin clatter
    k = tt(.5); x = np.convolve(r.standard_normal(len(k)), np.ones(80) / 80, 'same') * 6; m.f(x * g * .5, t - .45, 0)
    for i in range(10): m.clang(t + i * .035, .25 * g, r.uniform(-.6, .6))
m.vo('yamal', 'hmph', 0.5, .6, -.2); m.whip(1.6, .35); m.vo('generic_m', 'grunt', 1.8, .45, -.3); m.vo('generic_m', 'grunt', 2.1, .45, -.4)
for i in range(12): tap(3.1 + i * .26, .2); m.thump(3.2 + i * .26, .08)
m.vo('mbappe', 'laugh', 5.6, .45, .3, 'snicker')
m.whoosh(6.4, .5, .4); m.boom(6.6, .5); m.clang(6.8, .6, .3); m.xylo(7.0, ['C6', 'E6', 'G6', 'C7'], .07, .2); m.vo('generic_m', 'gasp', 7.2, .5, -.3)
for s0 in (9.2, 9.8): m.thump(s0, .5); m.whoosh(s0 + .03, .2, .3); m.spring(s0 + .25, .35); m.smack(s0 + .45, .6, -.3); m.vo('generic_m', 'ow', s0 + .5, .45, -.3)
m.whoosh(10.6, .45, .5); m.slide_whistle(10.62, True, .4, .2); m.bonk(11.05, .9); m.clang(11.06, .4, .2); m.vo('generic_m', 'oof', 11.1, .55, -.2)
m.whoosh(12.0, .6, .4); m.spring(12.6, .5, .9); m.vo('generic_m', 'yelp', 12.65, .5, -.2); m.thump(13.2, .5)
m.vo('yamal', 'grunt', 14.3, .55, 0); m.whoosh(14.6, .4, .35); m.clang(14.95, .7, .2); m.thump(15.2, .5); m.vo('yamal', 'ow', 15.25, .7, 0); m.vo('yamal', 'cry', 15.8, .55, 0, 'wail')
m.vo('mbappe', 'laugh', 16.2, .45, .4, 'belly'); m.whoosh(17.6, .5, .4); m.thump(17.95, .7); strike(18.1, .7); m.crowd(18.3, 'cheer', 1.5, .3); [m.vo('generic_m', 'yelp', 18.1 + i * .12, .35, -.4 + i * .2) for i in range(3)]
m.vo('yamal', 'cry', 20.9, .6, -.2, 'wail'); [tap(21.2 + i * .45, .2) for i in range(7)]; m.vo('yamal', 'cry', 22.6, .55, -.3, 'sob'); m.vo('generic_m', 'yay', 21.5, .45, .4); [m.cowbell(21.8 + i * .25, .12) for i in range(8)]
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [6.6, 9.65, 11.05, 14.95, 18.1], .45, .15, .4); d.room('fx', 'stadium', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
