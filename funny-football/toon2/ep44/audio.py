"""Ep44 v3 KEEP LAUGHING sound — fully synthesized. Funk bed; TV crowd + goal horn per goal; a 'ding' each time they set up a (wrong) defence;
a different slap per scorer; samba cowbells for Vinícius; ice-pack whimpers, remote click, five slaps in the dark, lights-on clunk, 'say cheese' + shutter, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 29.6; d = Desk(D); m = Mix2(D, ep=443)
song = Song('funk', key='E', minor=True, seed=443).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 3)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((22.8, 24.4, 0.0), (20.0, 21.0, 0.45)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(443)
def tt(dur): return np.arange(int(dur * SR)) / SR
def goalhorn(t, g=.3): k = tt(.7); m.f((np.sign(np.sin(2 * np.pi * 233 * k)) * .5 + np.sin(2 * np.pi * 349 * k) * .5) * np.minimum(1, k * 30) * np.minimum(1, (0.7 - k) * 10) * g * .5, t, .4)
def click(t, g=.3): k = tt(.03); m.f(r.standard_normal(len(k)) * np.exp(-k * 200) * g, t, .2)
def shutter(t, g=.5): k = tt(.12); m.f(r.standard_normal(len(k)) * np.exp(-k * 60) * g, t, 0); m.f(r.standard_normal(len(k)) * np.exp(-k * 50) * g * .7, t + .07, 0)
m.crowd(0.1, 'ooh', 1.2, .2); m.vo('generic_m', 'laugh', 0.4, .55, -.3, 'belly'); m.vo('yamal', 'laugh', 0.8, .6, .2, 'belly'); m.vo('generic_m', 'laugh', 1.9, .5, -.3, 'snicker')
GOALS = [(2.6, [1.6], 'none'), (6.1, [1.9, 2.25], 'guard'), (9.6, [1.9], 'look'), (13.1, [1.9, 2.2], 'cush'), (16.6, [1.8, 2.1, 2.4, 2.7], 'hats')]
WHO = {(1, 0): 'yamal', (1, 1): 'generic_m', (2, 0): 'yamal', (3, 0): 'generic_m', (3, 1): 'yamal', (4, 0): 'yamal', (4, 1): 'generic_m', (4, 2): 'yamal', (4, 3): 'generic_m', (0, 0): 'generic_m'}
for gi, (t0, hits, dfn) in enumerate(GOALS):
    m.crowd(t0, 'cheer', 1.3, .35); goalhorn(t0 + .05, .3); m.vo('yamal', 'gasp', t0 + .3, .45, .2)
    if dfn != 'none': m.xylo(t0 + .85, ['C6', 'G6'], .06, .16); m.vo('generic_m', 'hmm', t0 + 1.0, .4, -.2)   # "defence ready" ding
    if dfn == 'look': [m.whip(t0 + .9 + i * .25, .2) for i in range(2)]
    if dfn == 'hats': m.clang(t0 + .95, .35, -.2); m.clang(t0 + 1.1, .35, .2)
    m.whoosh(t0 + 1.0, .4, .25)
    for j, h in enumerate(hits):
        m.whoosh(t0 + h - .2, .2, .3); m.smack(t0 + h, .95 - j * .03, (-.3, .3)[j % 2]); m.vo(WHO[(gi, j)], 'ow', t0 + h + .05, .5, .1)
    if dfn == 'cush': m.cork(t0 + hits[0] + .05, .4); m.whoosh(t0 + hits[0] + .1, .4, .3)
m.vo('generic_m', 'hmph', 4.4, .5, -.4); m.vo('yamal', 'laugh', 4.8, .5, .2, 'snicker')
m.vo('mbappe', 'laugh', 11.7, .5, .4, 'snicker'); m.vo('mbappe', 'laugh', 15.4, .45, -.4, 'belly')
for i in range(12): m.cowbell(16.8 + i * .25, .14)
m.vo('generic_m', 'yay', 17.2, .5, .4)
m.vo('generic_m', 'cry', 20.2, .5, -.3, 'sob'); m.vo('yamal', 'cry', 20.5, .5, .2, 'sob'); click(20.9, .5); m.xylo(21.05, ['C6', 'G6'], .06, .15)
m.vo('yamal', 'laugh', 21.4, .55, .2, 'snicker'); m.vo('generic_m', 'laugh', 21.7, .5, -.3, 'snicker')
m.sub_boom(22.3, .5); m.timpani(22.4, 60, .35, .4); click(22.78, .6)
for i, a in enumerate((23.05, 23.35, 23.6, 23.9, 24.15)): m.smack(a, .95, (-.4, .4, 0, -.2, .2)[i]); m.vo('yamal' if i % 2 else 'generic_m', 'ow', a + .04, .45, 0)
click(24.4, .7); m.thump(24.42, .4); m.crowd(24.5, 'laugh', 1.6, .3); m.vo('mbappe', 'laugh', 24.6, .55, .4, 'belly'); m.xylo(24.9, ['E6', 'G6', 'C7'], .07, .18)
shutter(25.2, .7); m.vo('yamal', 'cry', 25.6, .5, 0, 'wail'); m.xylo_rise(26.0, .15)
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [4.2, 8.0, 8.35, 11.5, 15.0, 18.4, 25.2], .45, .15, .4); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
