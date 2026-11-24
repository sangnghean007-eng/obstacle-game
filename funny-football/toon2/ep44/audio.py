"""Ep44 KEEP LAUGHING sound — fully synthesized. Funk bed (new seed/key); TV crowd + goal horn for each Real goal,
Yamal/Raphinha laughing, a different slap for every scorer (Valverde single, Bellingham double, Mbappé 'Wake up', cushion poof, Vinícius samba slaps),
ice-pack whimpers, remote click, 5 slaps in the dark, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 27.8; d = Desk(D); m = Mix2(D, ep=44)
song = Song('funk', key='E', minor=True, seed=44).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 3)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((24.2, 26.0, 0.0), (19.6, 21.4, 0.45)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(44)
def tt(dur): return np.arange(int(dur * SR)) / SR
def goalhorn(t, g=.3): k = tt(.7); m.f((np.sign(np.sin(2 * np.pi * 233 * k)) * .5 + np.sin(2 * np.pi * 349 * k) * .5) * np.minimum(1, k * 30) * np.minimum(1, (0.7 - k) * 10) * g * .5, t, .4)
def click(t, g=.3): k = tt(.03); m.f(r.standard_normal(len(k)) * np.exp(-k * 200) * g, t, .2)
# A: they laugh at 0-1
m.crowd(0.1, 'ooh', 1.4, .2); m.vo('generic_m', 'laugh', 0.5, .55, -.3, 'belly'); m.vo('yamal', 'laugh', 0.9, .6, .2, 'belly'); m.vo('generic_m', 'laugh', 2.0, .5, -.3, 'snicker')
GOALS = [(3.0, [1.6]), (6.4, [1.5, 1.85]), (9.8, [1.7]), (13.4, [1.4, 1.9, 2.2]), (16.4, [1.4, 1.75, 2.1, 2.45])]
for gi, (t0, hits) in enumerate(GOALS):
    m.crowd(t0, 'cheer', 1.4, .35); goalhorn(t0 + .05, .3); m.vo('yamal', 'gasp', t0 + .3, .45, .2)
    m.whoosh(t0 + .6, .4, .25)                                                     # the scorer sneaks in
    for j, h in enumerate(hits):
        m.whoosh(t0 + h - .18, .2, .3)
        if gi == 3 and j == 0: m.cork(t0 + h, .5); m.whoosh(t0 + h + .02, .5, .35)  # cushions POOF
        else: m.smack(t0 + h, .95 - j * .03, (-.3, .3)[j % 2]); m.vo('yamal' if (gi in (2, 3, 4) and j % 2 == (0 if gi == 2 else 1)) else 'generic_m', 'ow', t0 + h + .05, .5, .1)
m.vo('generic_m', 'hmph', 4.7, .5, -.4, ); m.vo('yamal', 'laugh', 5.2, .5, .2, 'snicker')     # Yamal still laughs at Raphinha
m.vo('mbappe', 'laugh', 10.6, .5, .4, 'snicker'); m.vo('mbappe', 'hmm', 11.2, .45, .4)       # "Wake up!" beat (caption)
m.vo('mbappe', 'laugh', 14.5, .45, .4, 'belly')
for i in range(12): m.cowbell(16.6 + i * .25, .14)                                          # Vinícius samba
m.vo('generic_m', 'yay', 17.0, .5, .4)
# G: ice packs, remote, laughing again
m.vo('generic_m', 'cry', 19.8, .5, -.3, 'sob'); m.vo('yamal', 'cry', 20.2, .5, .2, 'sob'); click(21.3, .5); m.xylo(21.45, ['C6', 'G6'], .06, .15)
m.vo('yamal', 'laugh', 21.9, .55, .2, 'snicker'); m.vo('generic_m', 'laugh', 22.3, .5, -.3, 'snicker')
# H: shadows, lights out, five slaps in the dark
m.sub_boom(23.6, .5); m.timpani(23.7, 60, .35, .4); click(24.15, .6)
for i, a in enumerate((24.45, 24.75, 25.0, 25.3, 25.55)): m.smack(a, .95, (-.4, .4, 0, -.2, .2)[i]); m.vo('yamal' if i % 2 else 'generic_m', 'ow', a + .04, .45, 0)
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [4.6, 7.9, 8.25, 11.5, 15.3, 17.8, 18.5], .45, .15, .4); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
