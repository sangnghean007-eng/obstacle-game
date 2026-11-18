"""Ep19 WE DON'T NEED HIM sound: Portuguese-guitar-flavoured strum (fado-ish, original) for Portugal, oompah tuba for the Saudi sofa, stadium bits.
New this episode: poster rip, bulldozer rumble, popcorn burst, TV crack, card whistles. vox2/fx2 only.
hook 0 · denmark 3.2 · sofa1 7.4 · wales 10.4 · sofa2 16.4 · mock 20.0 · end 23.4 · END 27.6"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 31.2; m = Mix2(END, ep=19)
def fado(t0, t1, g=.6, bpm=132):
    b = 60 / bpm; t = t0; i = 0; ch = [['A3', 'C4', 'E4'], ['E3', 'G#3', 'B3'], ['D3', 'F3', 'A3'], ['E3', 'G#3', 'B3']]; mel = ['E5', 'C5', 'A4', 'B4', 'C5', 'D5', 'E5', 'B4']
    while t < t1 - .02:
        for k, n in enumerate(ch[(i // 4) % 4]): m.pluck(hz(n), t + k * .015, .3, .1 * g, -.2, 1.3)
        if i % 2 == 0: m.pluck(hz(mel[(i // 2) % 8]), t, .25, .14 * g, .3, 1.6)
        t += b / 2; i += 1
def whistle(t, n=1, g=.3):
    for k in range(n): d = .22 if n > 1 else .4; tt = T(d); m.f(osc(2800 * (1 + .03 * np.sin(2 * np.pi * 40 * tt)), d) * env(len(tt), .01, .03), t + k * .3, g, 0, .2)
def roar(t, g=.4, d=1.6): m.crowd(t, 'cheer', d, g)
def rip(t): d = .45; m.f(bp(noise(d), 1500, 7000) * env(int(d * SR), .01, .08) * (1 + .8 * np.sin(2 * np.pi * 60 * T(d))), t, .6)
# HOOK
fado(0, 3.2, .7); m.vo('bruno', 'grunt', .8, .5); rip(1.0); m.crowd(1.1, 'cheer', 1.6, .4); m.cork(1.15, .3); m.vo('bruno', 'laugh', 1.5, .5, 0, 'point')
# DENMARK: bulldozer rumble x2, flattened oofs, crowd groans
t = 3.2; whistle(t)
for a in (.4, 2.0):
    m.f(lp(noise(.9), 180) * env(int(.9 * SR), .1, .1) * (1 + .5 * np.sin(2 * np.pi * 9 * T(.9))), t + a, .6)
    for i, who in enumerate(('generic_m', 'big', 'bruno')): m.smack(t + a + .3 + i * .18, .6, (-1) ** i * .3); m.vo(who, 'oof', t + a + .32 + i * .18, .5)
    m.thump(t + a + .9, .6); m.vo('hojlund', 'yay', t + a + 1.0, .5)
m.crowd(t + 3.0, 'gasp', 1.0, .35); m.wahwah(t + 3.3, .2)
# SOFA 1: oompah, Ronaldo laughs, falls off the sofa
t = 7.4; m.oompah(t, t + 3.0, ('F2', 'C2'), 128, .7); m.vo('ronaldo', 'laugh', t + .3, .7, 0, 'belly', 1.4); m.vo('ronaldo', 'laugh', t + 1.4, .6, 0, 'cackle'); m.thump(t + 2.0, .7); m.vo('ronaldo', 'oof', t + 2.02, .6)
for i in range(6): m.pop(t + 2.05 + i * .05, .15, 900 + i * 120)
# WALES: fast montage, two goals each, cards
t = 10.4; whistle(t); fado(t, t + 6.0, .55, 150)
for a, team in ((.6, 'P'), (1.6, 'W'), (2.6, 'W'), (3.6, 'P')): m.thwack(a + t - .1, .6); m.thump(t + a, .5); roar(t + a, .4 if team == 'P' else .3, 1.2)
m.boom(t + .55, .35)
whistle(t + 4.4, 1, .35); whistle(t + 4.7, 1, .35); whistle(t + 4.9, 3, .4); m.vo('generic_m', 'no', t + 4.95, .5); m.slide_whistle(t + 5.0, True, .7, .35); m.crowd(t + 5.0, 'gasp', 1.0, .3)
# FORBS: sub beep, the winner, pile-on
t = 16.4; m.f(osc(1000, .15, 'sq') * env(int(.15 * SR), .005, .02), t + .05, .15); m.f(osc(1000, .15, 'sq') * env(int(.15 * SR), .005, .02), t + .25, .15)
m.thwack(t + 1.2, .8); m.whoosh(t + 1.25, .35, .3); m.thump(t + 1.6, .6); roar(t + 1.6, .55, 1.4); m.vo('forbs' if False else 'kid', 'yay', t + 1.7, .6); m.thump(t + 2.4, .5)
# SOFA 2: "who?" laugh → POP → bucket → CRACK
t = 19.4; m.oompah(t, t + 1.8, ('F2', 'C2'), 128, .6); m.vo('ronaldo', 'laugh', t + .3, .6, 0, 'snicker', 1.2); roar(t + 1.75, .35, 1.0)
m.boom(t + 1.8, .4); [m.pop(t + 1.8 + i * .03, .2, 700 + i * 90) for i in range(12)]; m.vo('ronaldo', 'yelp', t + 1.85, .7); m.thump(t + 2.0, .5); m.whoosh(t + 2.4, .2, .25); m.clang(t + 2.6, .4); m.f(hp(noise(.3), 3000) * dec(.3, 15), t + 2.6, .6); m.vo('ronaldo', 'cry', t + 2.8, .6, 0, 'wail', .8)
# MOCK: four SIUUU jumps (each a different voice), crowd laughs
t = 23.0; fado(t, t + 3.4, .8, 140)
for i, who in enumerate(('generic_m', 'big', 'bruno', 'kid')): m.whoosh(t + .3 + i * .35, .3, .2, True); m.vo(who, 'siu', t + .55 + i * .35, .5, -.5 + i * .33); m.thump(t + .9 + i * .35, .4)
m.crowd(t + 2.0, 'laugh', 1.4, .35)
# END: sobbing under the bucket, sad kazoo
t = 26.4; m.vo('ronaldo', 'cry', t + .2, .6, 0, 'blubber', 1.6); m.vo('ronaldo', 'cry', t + 2.0, .5, 0, 'sob', 1.4); m.kazoo(t + 1.0, ['E4', 'D#4', 'D4', 'C#4'], .3, .12); m.crowd(t + 1.6, 'laugh', 1.6, .15, .5)
m.write(sys.argv[1])
