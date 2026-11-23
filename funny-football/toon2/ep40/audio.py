"""Ep40 v4 "Who Laughs Last" sound — fully synthesized (ElevenLabs credits out until ~3 Dec).
Lo-fi living-room bed + one rising 'HEHEHE' that grows every time; each missed ball that leaves the TV gets its own big sound:
glass crack (Ronaldo), ceiling crash (Mbappé), slow roll (Yamal)."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 29.4; d = Desk(D); m = Mix2(D, ep=404)
song = Song('lofi', key='F', minor=False, seed=404).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 3)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((0.3, 1.6, 0.35), (2.7, 3.4, 0.3), (8.6, 9.8, 0.3), (11.3, 12.6, 0.15), (18.2, 19.4, 0.3), (21.4, 22.8, 0.05)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(404)
def tt(dur): return np.arange(int(dur * SR)) / SR
def whistle(t, dur=.35, g=.3):
    k = tt(dur); x = np.sin(2 * np.pi * 3050 * k) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * k)) * np.minimum(1, k * 40) * np.minimum(1, (dur - k) * 30); m.f(x * g, t, .3)
def glass(t, g=.7):  # shatter: bright noise bursts + tinkles
    k = tt(.9); m.f(r.standard_normal(len(k)) * np.exp(-k * 7) * g * .6, t, 0)
    for i in range(14): f = r.uniform(2500, 6500); kk = tt(.18); m.f(np.sin(2 * np.pi * f * kk) * np.exp(-kk * 30) * g * .35, t + .05 + i * .045, 0)
def popcorn(t, n=22, g=.3):
    for i in range(n): kk = tt(.04); m.f(r.standard_normal(len(kk)) * np.exp(-kk * 120) * g, t + r.uniform(0, .7), r.uniform(-.6, .6))
def roll(t, dur=1.0, g=.35):
    k = tt(dur); x = r.standard_normal(len(k)); x = np.convolve(x, np.ones(60) / 60, 'same') * (1 + .5 * np.sin(2 * np.pi * 7 * k)) * np.exp(-k * 1.5); m.f(x * g * 4, t, .3)
def hehe(who, t, n, g=.6, pan=0):
    for i in range(n): m.vo(who, 'laugh', t + i * .5, g, pan, 'snicker')
# Ronaldo: run, post, ball at the camera, glass breaks, he blames himself
whistle(0.0, .3); m.thump(0.2, .12); m.thump(0.35, .12); m.thump(0.5, .7); m.clang(0.8, .8, .3); m.whoosh(0.85, .55, .5); m.thump(1.33, .6); glass(1.35, .8)
m.crowd(1.5, 'ooh', 1.2, .4); m.vo('ronaldo', 'no', 1.6, .7, 0); m.vo('ronaldo', 'cry', 2.1, .5, 0)
# the ball comes out of the TV into the popcorn
m.whoosh(2.72, .35, .45); m.thump(3.05, .6); m.cork(3.05, .5); popcorn(3.05, 26, .35); m.vo('mbappe', 'gasp', 3.2, .5, .3)
hehe('yamal', 3.6, 3, .65, -.3); m.vo('mbappe', 'hmph', 5.0, .6, .3)
# Mbappé: for my idol
m.whoosh(6.0, .35, .3); m.timpani(6.2, 98, .4); m.vo('mbappe', 'grunt', 6.4, .55, .2); popcorn(6.3, 9, .2); m.xylo_rise(7.0, .18)
# Mbappé's pen: skied
whistle(8.35, .35); [m.thump(8.5 + i * .17, .12) for i in range(4)]; m.thump(9.2, .7); m.whoosh(9.25, 1.1, .45); m.slide_whistle(9.3, True, 1.0, .3); m.crowd(9.6, 'ooh', 1.3, .4); m.vo('mbappe', 'no', 9.9, .6, .1)
# ...and it comes down through the ceiling
[m.thump(11.4 + i * .09, .12) for i in range(6)]; m.slide_whistle(11.5, False, .4, .25); m.boom(11.9, .6); m.thump(12.25, .8); m.spring(12.3, .35)
[m.thump(12.0 + i * .07, .1) for i in range(8)]; m.vo('yamal', 'gasp', 12.0, .5, -.3)
hehe('yamal', 12.6, 4, .7, -.1); m.squeak(13.25, .3)
# Yamal takes Raphinha's ball: watch this
m.crowd(14.6, 'cheer', 1.0, .25); m.whoosh(15.0, .4, .35); m.whip(15.4, .45); m.vo('generic_m', 'gasp', 15.5, .5, .3); m.vo('yamal', 'laugh', 15.9, .5, -.2, 'snicker'); m.cowbell(16.6, .15)
# Yamal's pen: shank, rolls at the camera
whistle(18.0, .35); [m.thump(18.15 + i * .17, .12) for i in range(4)]; m.squeak(18.8, .45); m.thump(18.82, .35); m.fail_horn(19.0, .22); m.crowd(19.3, 'ooh', 1.3, .35)
# ...and rolls out of the TV to Ronaldo and Mbappé
roll(20.8, 1.0, .4); m.thump(21.75, .2); m.record_scratch(21.6, .45); m.timpani(21.6, 70, .3); m.zip(22.2, .2); m.zip(22.35, .2)
m.smack(22.8, .6); [m.whoosh(x, .25, .25) for x in (2.7, 8.3, 11.0, 14.6, 20.6)]; hehe('ronaldo', 22.9, 4, .6, -.35); hehe('mbappe', 23.1, 4, .6, .35); m.crowd(23.4, 'laugh', 1.6, .2)
# Yamal climbs out of the TV
m.sub_boom(24.7, .7); m.slide_whistle(24.9, True, .7, .25); m.vo('yamal', 'cry', 25.6, .55, 0, 'wail'); [m.smack(26.4 + i * .25, .35) for i in range(3)]
hehe('ronaldo', 27.2, 3, .45, -.4); hehe('mbappe', 27.4, 3, .45, .4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [0.8, 1.35, 3.05, 9.2, 11.9, 18.8], .45, .15, .4); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
