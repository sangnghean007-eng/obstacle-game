"""Ep41 TUG OF WAR sound — fully synthesized. Trap bed (new seed/key), rope creaks and strain grunts,
9 'heave' tugs that move nothing, dust skid, the comeback yank, two penalty misses, 'MY ROPE', laugh vs cry ending."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 28.6; d = Desk(D); m = Mix2(D, ep=41)
song = Song('trap', key='G', minor=True, seed=41).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((6.4, 7.2, 0.3), (9.6, 10.2, 0.2), (20.6, 21.1, 0.15), (22.7, 24.0, 0.25)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(41)
def tt(dur): return np.arange(int(dur * SR)) / SR
def creak(t, g=.25):  # rope creak: slow pitch wobble through a bandpass
    k = tt(.4); f = 180 + 60 * np.sin(2 * np.pi * 3 * k); x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-k * 4); m.f(x * g * .3, t, 0)
def skid(t, dur=2.4, g=.3):
    k = tt(dur); x = r.standard_normal(len(k)); x = np.convolve(x, np.ones(25) / 25, 'same') * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * k)); m.f(x * g * 3, t, -.4)
m.crowd(0.1, 'cheer', 2.0, .3)
for i in range(6): creak(0.3 + i * 0.35, .2)
m.vo('generic_m', 'grunt', 1.0, .4, -.4); m.vo('mbappe', 'grunt', 1.5, .4, .4)
# B: 9 tugs, nothing moves
for i, a in enumerate([2.8 + j * 0.4 for j in range(9)]): m.thump(a, .45 + i * .03); creak(a + .05, .25); m.vo('mbappe', 'grunt', a + .02, .35 + i * .02, .4)
m.xylo(5.0, ['C5', 'E5', 'G5', 'C6'], .07, .15); m.wahwah(5.7, .2); m.vo('yamal', 'laugh', 5.2, .45, -.3, 'snicker')
# C: Barça dragged (0-2)
skid(6.6, 2.8, .35); m.slide_whistle(6.7, False, 1.4, .25); m.vo('yamal', 'yelp', 6.9, .5, -.3); m.vo('generic_m', 'gasp', 7.3, .45, -.4); m.crowd(7.6, 'ooh', 1.5, .3); m.vo('mbappe', 'laugh', 8.2, .45, .4, 'snicker')
# D: the comeback yank
m.timpani(9.6, 80, .45, .5); m.whip(10.0, .6); m.boom(10.05, .6); m.thump(10.3, .7); m.thump(10.45, .5); m.vo('mbappe', 'oof', 10.3, .6, .4); m.crowd(10.2, 'cheer', 2.0, .45); m.sub_boom(10.0, .5)
# E: Mbappé lets go — penalty skied
m.whoosh(12.4, .3, .3); m.vo('mbappe', 'hmm', 12.6, .4, .3); m.thump(13.2, .7); m.whoosh(13.25, 1.0, .45); m.slide_whistle(13.3, True, 1.0, .28); m.crowd(13.6, 'ooh', 1.3, .35); m.vo('mbappe', 'no', 13.9, .6, .3)
# F: Yamal lets go — penalty wide
m.whoosh(15.4, .3, .3); m.squeak(16.2, .45); m.thump(16.22, .3); m.fail_horn(16.5, .2); m.vo('yamal', 'uhoh', 16.9, .5, -.3)
# MY ROPE
m.record_scratch(17.0, .4); m.vo('generic_m', 'hmph', 17.1, .65, -.2); creak(17.4, .3); creak(17.9, .3)
# G: Yamal offers the cup… snatches it back, slaps Mbappé awake, turns his head to the table; laugh vs cry
m.crash(18.6, .25); m.crowd(18.7, 'cheer', 1.4, .3); m.vo('mbappe', 'cry', 18.8, .45, .4, 'wail')
m.xylo(19.4, ['C5', 'E5', 'G5'], .09, .15); m.vo('yamal', 'hmm', 19.5, .45, -.2); m.vo('mbappe', 'yay', 20.05, .6, .3)
m.whip(20.6, .6); m.record_scratch(20.62, .45); m.vo('yamal', 'laugh', 20.8, .45, -.2, 'snicker')
for i, a in enumerate((21.0, 21.35, 21.7)): m.smack(a, .9 - i * .05, (-.3, .3)[i % 2]); m.vo('mbappe', 'ow', a + .04, .5, .3)
m.spring(21.95, .3); m.whoosh(22.2, .4, .35); m.squeak(22.3, .35); m.sub_boom(22.8, .6); m.timpani(22.85, 70, .4, .6); m.vo('mbappe', 'gasp', 23.0, .55, .3)
m.crowd(24.1, 'laugh', 2.4, .35); m.vo('yamal', 'laugh', 24.2, .6, -.4, 'belly'); m.vo('generic_m', 'laugh', 24.4, .55, -.5, 'belly'); m.vo('mbappe', 'cry', 24.5, .65, .4, 'wail'); m.fail_horn(25.2, .18)
m.vo('mbappe', 'cry', 26.2, .55, .4, 'sob'); m.vo('yamal', 'laugh', 26.6, .45, -.4, 'snicker'); m.xylo_rise(27.4, .15)
m.cta(28.6 - 2.4)  # end-card support call (cta2.js)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [10.0, 13.2, 16.2, 17.0, 20.6, 21.0, 22.8], .45, .15, .4); d.room('fx', 'stadium', .15)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
