"""Ep46 THE BAR sound — fully synthesized. Noir-jazz bed (new seed/key) that sinks with the bar; triumphant fanfare for 1999 and 2013,
a CLUNK + falling tone for each lower 'standard', strain grunts while Bruno carries everyone, trip thud, VAR beeps + record scratch, red-card whistle,
megaphone 'SO PROUD!' squeal, crickets, shovel digs, sad trombone, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 29.4; d = Desk(D); m = Mix2(D, ep=46)
song = Song('noirjazz', key='C', minor=True, seed=46).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 3)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((0, 5.4, 0.35), (19.8, 21.8, 0.08)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(46)
def tt(dur): return np.arange(int(dur * SR)) / SR
def fanfare(t, g=.3, notes=(392, 523, 659, 784)):
    for i, f in enumerate(notes): k = tt(.16 if i < 3 else .5); m.f((np.sign(np.sin(2 * np.pi * f * k)) * .5 + np.sin(2 * np.pi * f * 2 * k) * .3) * np.minimum(1, k * 40) * np.minimum(1, ((.16 if i < 3 else .5) - k) * 20) * g * .5, t + i * .14, .2)
def fall(t, g=.25): k = tt(.5); m.f(np.sin(2 * np.pi * np.cumsum(900 - 600 * k / .5) / SR) * np.exp(-k * 3) * g, t, 0)
def whistle(t, dur=.5, g=.3): k = tt(dur); m.f(np.sin(2 * np.pi * 3000 * k) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * k)) * np.minimum(1, k * 40) * np.minimum(1, (dur - k) * 30) * g, t, .3)
def beep(t, f=1400, g=.25): k = tt(.12); m.f(np.sign(np.sin(2 * np.pi * f * k)) * np.minimum(1, (0.12 - k) * 60) * g * .4, t, .3)
def cricket(t0, t1, g=.12):
    t = t0
    while t < t1: k = tt(.18); m.f(np.sin(2 * np.pi * 4300 * k) * (np.sin(2 * np.pi * 40 * k) > 0) * np.exp(-k * 8) * g, t, .5); t += .45
def dig(t, g=.3): k = tt(.2); m.f(np.convolve(r.standard_normal(len(k)), np.ones(15) / 15, 'same') * np.exp(-k * 18) * g * 4, t, -.3)
m.crowd(0.2, 'cheer', 2.6, .4); m.whoosh(1.3, .8, .4); fanfare(2.0, .35); m.vo('generic_m', 'yay', 2.2, .5, 0)
m.whoosh(4.2, .7, .35); m.crowd(4.6, 'cheer', 1.0, .3); fanfare(4.8, .25, (392, 494, 587, 784))
for a in (6.0, 7.0, 8.0, 9.0): m.thump(a, .6); m.clang(a + .02, .35, 0); fall(a + .05, .22)
m.thump(9.6, .8); fall(9.65, .3); m.wahwah(10.2, .2); m.vo('generic_m', 'grunt', 10.9, .5, 0)   # Bruno arrives, chest thump
m.thump(11.0, .35); m.thump(11.25, .35)
for g0 in (12.6, 13.6): [m.thump(g0 - .6 + i * .15, .15) for i in range(3)]; m.spring(g0 - .3, .2); m.thump(g0, .7); m.whoosh(g0 + .03, .5, .4); m.crowd(g0 + .1, 'cheer', 1.0, .35); m.vo('generic_m', 'yay', g0 + .2, .5, 0)
m.vo('generic_m', 'yelp', 14.8, .5, -.3); m.thump(14.95, .7); m.smack(15.0, .5); m.vo('generic_m', 'no', 15.1, .6, 0)          # trip → Bruno complains
m.vo('generic_m', 'yay', 16.4, .55, -.3); [beep(16.8 + i * .2) for i in range(3)]; m.record_scratch(17.0, .45); m.vo('generic_m', 'gasp', 17.1, .6, 0)
whistle(18.0, .6, .35); m.vo('generic_m', 'cry', 18.6, .6, 0, 'wail')
m.f(np.sin(2 * np.pi * 2400 * tt(.3)) * .15 * np.exp(-tt(.3) * 3), 19.85, .2); m.vo('generic_m', 'yay', 19.95, .7, .3); cricket(20.35, 21.9, .18)
for i in range(4): dig(22.0 + i * .4, .3)
m.vo('generic_m', 'hmm', 23.2, .55, 0); m.thump(23.5, .5); m.vo('generic_m', 'grunt', 23.6, .5, 0); [m.thump(24.0 + i * .5, .2) for i in range(6)]
m.fail_horn(25.2, .2); m.timpani(26.4, 55, .3, .3)
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [2.0, 4.8, 9.6, 12.6, 13.6, 14.95, 17.0, 18.0], .45, .15, .4); d.room('fx', 'stadium', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
