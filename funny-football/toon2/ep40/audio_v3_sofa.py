"""Ep40 v3 "Who Laughs Last" sound — fully synthesized (ElevenLabs credits out until ~3 Dec):
lo-fi living-room bed (new seed/key), TV-broadcast whistles + crowd, post CLANG, the running 'HEHEHE' laugh (escalates each time), vox2 for Ronaldo / Mbappé / Yamal."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 29.4; d = Desk(D); m = Mix2(D, ep=403)
song = Song('lofi', key='F', minor=False, seed=403).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 3)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((2.6, 3.9, 0.3), (11.0, 12.3, 0.3), (20.0, 21.3, 0.3), (6.0, 8.4, 0.55), (14.4, 16.6, 0.55), (23.0, 26.0, 0.55)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(403)
def tt(dur): return np.arange(int(dur * SR)) / SR
def whistle(t, dur=.35, g=.3):
    k = tt(dur); x = np.sin(2 * np.pi * 3050 * k) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * k)) * np.minimum(1, k * 40) * np.minimum(1, (dur - k) * 30); m.f(x * g, t, .3)
def munch(t, n=4, g=.12):
    for i in range(n): k = tt(.06); m.f(r.standard_normal(len(k)) * np.exp(-k * 60) * g, t + i * .17, -.2)
def hehe(who, t, n, g=.6, pan=0):  # the running laugh: more 'HE's each time
    for i in range(n): m.vo(who, 'laugh', t + i * .55, g, pan, 'snicker')
def tvon(t, g=.25):
    k = tt(.25); m.f(np.sin(2 * np.pi * 15600 * k) * np.exp(-k * 10) * g * .3 + r.standard_normal(len(k)) * np.exp(-k * 30) * g, t, 0)
# A — sofa, popcorn, TV on
tvon(0.05); munch(0.6); m.vo('yamal', 'hmm', 1.4, .4, -.3); munch(1.8, 3)
# B — TV: Ronaldo pen hits the post, he blames himself
m.crowd(2.4, 'cheer', 1.0, .25); whistle(2.5, .4); [m.thump(2.7 + i * .18, .12) for i in range(4)]; m.thump(3.4, .7); m.whoosh(3.42, .3, .35)
m.clang(3.7, .7, .4); m.crowd(3.8, 'ooh', 1.6, .45); m.vo('ronaldo', 'no', 4.0, .7, .1); m.vo('ronaldo', 'cry', 4.7, .5, 0, 'sob'); m.thump(4.75, .3)
# C — Yamal: HEHEHE; Mbappé fumes
tvon(6.0, .15); hehe('yamal', 6.25, 3, .65, -.3); m.vo('mbappe', 'hmph', 7.3, .6, .3); m.honk(7.9, .18)
# D — Mbappé stands: for my idol
m.whoosh(8.4, .35, .3); m.timpani(8.6, 98, .4); m.vo('mbappe', 'grunt', 8.7, .55, .3); m.xylo_rise(9.2, .18); m.vo('yamal', 'hmm', 10.2, .4, -.3)
# E — TV: Mbappé skies it
m.crowd(10.8, 'cheer', 1.0, .25); whistle(10.9, .4); [m.thump(11.1 + i * .18, .12) for i in range(4)]; m.thump(11.8, .7); m.whoosh(11.85, 1.2, .45); m.slide_whistle(11.9, True, 1.1, .3)
m.crowd(12.2, 'ooh', 1.6, .45); m.vo('mbappe', 'no', 12.4, .7, .1); m.wahwah(13.2, .22)
# F — Yamal laughs harder, rolls over
tvon(14.4, .15); hehe('yamal', 14.6, 4, .7, -.1); m.thump(15.6, .35); m.squeak(15.7, .3)
# G — TV: Yamal grabs the ball from Raphinha
m.crowd(16.6, 'cheer', 1.0, .25); m.whoosh(17.0, .4, .35); m.whip(17.4, .45); m.vo('generic_m', 'gasp', 17.5, .5, .3); m.vo('yamal', 'laugh', 17.9, .5, -.2, 'snicker'); m.cowbell(18.6, .15)
# H — Yamal's pen rolls wide
whistle(19.9, .4); [m.thump(20.1 + i * .18, .12) for i in range(4)]; m.squeak(20.8, .45); m.thump(20.82, .35); m.kazoo(21.1, ['A4', 'G4', 'F4', 'E4'], .25, .15)
m.crowd(21.3, 'ooh', 1.6, .4); m.vo('yamal', 'uhoh', 21.6, .55, 0)
# I — now Ronaldo and Mbappé laugh (who laughs last)
tvon(23.0, .15); hehe('ronaldo', 23.2, 4, .6, -.35); hehe('mbappe', 23.45, 4, .6, .35); m.crowd(24.0, 'laugh', 1.8, .25)
# J — Yamal squeezed in the middle; POST / WIDE / SKY stamps
m.whoosh(26.0, .4, .3); m.thump(26.35, .7); m.vo('yamal', 'hmph', 26.6, .6, 0); [m.smack(26.4 + i * .25, .35) for i in range(3)]
m.vo('yamal', 'cry', 27.3, .5, 0, 'wail'); hehe('ronaldo', 27.9, 2, .45, -.4); hehe('mbappe', 28.1, 2, .45, .4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [3.4, 3.7, 11.8, 20.8, 26.35], .45, .15, .4); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
