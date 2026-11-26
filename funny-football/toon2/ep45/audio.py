"""Ep45 v2 DEBT COLLECTORS sound — fully synthesized. Western stand-off bed; march taps; shield CLANG entrance; BOINK x2; Adeyemi rocket + SPLAT;
pyramid grunts + shield 'grow' rising tone + a tiny TAP + CRASH; crutch CLANG on his own ankle; bowling STRIKE; sob walk home; rolling shield rumble + SPLAT; pop-up 'boing'; CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 26.4; d = Desk(D); m = Mix2(D, ep=452)
song = Song('western', key='D', minor=True, seed=452).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((4.6, 5.4, 0.25), (12.1, 12.9, 0.15), (14.6, 15.4, 0.25), (19.9, 20.8, 0.2)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(452)
def tt(dur): return np.arange(int(dur * SR)) / SR
def tap(t, g=.25): k = tt(.06); m.f(np.sin(2 * np.pi * 900 * k) * np.exp(-k * 80) * g, t, -.3)
def rise(t, dur=.6, g=.3): k = tt(dur); m.f(np.sin(2 * np.pi * np.cumsum(200 + 900 * k / dur) / SR) * np.sin(np.pi * k / dur) * g * .5, t, .3)
def rumble(t0, t1, g=.4): k = tt(t1 - t0); x = np.convolve(r.standard_normal(len(k)), np.ones(90) / 90, 'same') * 8 * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * k)); m.f(x * g, t0, 0)
def strike(t, g=.6): rumble(t - .45, t, g * .6); [m.clang(t + i * .035, .25 * g, r.uniform(-.6, .6)) for i in range(10)]
m.vo('yamal', 'hmph', 0.4, .6, -.2); m.whip(1.4, .35); m.vo('generic_m', 'grunt', 1.6, .45, -.3); m.vo('generic_m', 'grunt', 1.9, .45, -.4)
for i in range(8): tap(2.5 + i * .26, .2); m.thump(2.6 + i * .26, .08)
m.whoosh(4.6, .5, .4); m.boom(4.8, .5); m.clang(5.0, .6, .3); m.xylo(5.2, ['C6', 'E6', 'G6', 'C7'], .07, .2); m.vo('mbappe', 'laugh', 5.6, .45, .3, 'snicker')
for s0 in (6.8, 7.4): m.thump(s0, .5); m.whoosh(s0 + .03, .2, .3); m.spring(s0 + .25, .35); m.smack(s0 + .45, .6, -.3); m.vo('generic_m', 'ow', s0 + .5, .45, -.3)
m.whoosh(8.4, .4, .5); m.slide_whistle(8.42, True, .35, .2); m.smack(8.8, 1.0); m.thump(8.82, .6); m.vo('generic_m', 'oof', 8.85, .55, 0); m.slide_whistle(9.6, False, .6, .22)
[m.vo('generic_m', 'grunt', 10.4 + i * .25, .4, -.2 + i * .2) for i in range(3)]; m.xylo(10.9, ['C5', 'E5', 'G5'], .1, .16)
rise(11.4, .55, .45); m.timpani(11.5, 70, .4); m.vo('generic_m', 'gasp', 11.9, .45, -.2)
tap(12.2, .35); m.xylo(12.22, ['C7'], .05, .15); [m.vo('generic_m', 'yelp', 12.5 + i * .1, .35, -.4 + i * .3) for i in range(3)]; m.thump(12.85, .7); m.boom(12.9, .45)
m.vo('yamal', 'grunt', 14.2, .55, 0); m.whoosh(14.45, .4, .35); m.clang(14.55, .7, .2); m.thump(14.8, .5); m.vo('yamal', 'ow', 14.85, .7, 0); m.vo('yamal', 'cry', 15.2, .5, 0, 'wail')
m.whoosh(15.8, .5, .4); m.thump(16.15, .7); strike(16.3, .7); m.crowd(16.5, 'cheer', 1.2, .25)
m.vo('yamal', 'cry', 17.6, .55, -.2, 'sob'); [tap(17.8 + i * .45, .18) for i in range(5)]
m.thump(18.35, .6); m.whoosh(18.4, .3, .3); m.vo('mbappe', 'laugh', 18.6, .45, .3, 'snicker'); rumble(18.5, 20.0, .5); m.vo('yamal', 'uhoh', 19.5, .5, -.2)
m.smack(20.0, 1.0); m.boom(20.02, .5); m.slide_whistle(20.1, False, .5, .25); m.record_scratch(20.15, .3)
m.spring(21.0, .5, .8); m.vo('yamal', 'cry', 21.2, .7, -.2, 'wail'); m.crowd(21.4, 'laugh', 1.6, .3); [m.cowbell(21.6 + i * .25, .12) for i in range(8)]; m.vo('generic_m', 'yay', 21.8, .45, .4)
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [5.0, 7.25, 8.8, 12.85, 14.55, 16.3, 20.0], .45, .15, .4); d.room('fx', 'stadium', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
