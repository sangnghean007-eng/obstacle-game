"""Ep16 THE TEAM PHOTO sound: sneaky heist beat, stamps, slingshot snap, flick, ladder crash, golazo, bowling strike, shutter. No TTS.
hook 0 · disguise 3 · flick 8 · ladder 12.5 · ball 16.5 · cry 20.5 · flash 23 · photo 30 · end 36"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
OLD = [(0, 3), (3, 5), (8, 4.5), (12.5, 4), (16.5, 4), (20.5, 2.5), (23, 7), (30, 6)]
NEWD = [3, 5, 4.5, 4, 3, 2.5, 5.4, 4.5]
NEW0 = [sum(NEWD[:i]) for i in range(len(NEWD))]
def R(t):
    for (a_, d_), n0 in zip(OLD, NEW0):
        if t < a_ + d_: return n0 + (t - a_)
    return NEW0[-1] + (t - OLD[-1][0])
END = sum(NEWD); m = Mix2(END, ep=16)
_put = m.put; m.put = lambda bus, s, t0, *a, **k: _put(bus, s, R(t0), *a, **k)
def sneak(t0, t1, g=.7, bpm=104):
    b = 60 / bpm; t = t0; i = 0; notes = ['E3', None, 'G3', None, 'E3', 'D#3', 'E3', None, 'B2', None, 'C3', None, 'D#3', None, 'E3', None]
    while t < t1 - .02:
        if i % 4 == 0: m.kick(t, .4 * g)
        if i % 4 == 2: m.snare(t, .15 * g)
        n = notes[i % 16]
        if n: m.pluck(hz(n), t, .2, .22 * g)
        m.hat(t + b / 2, .05 * g); t += b / 2 * 2 if False else b / 2; i += 1
def fight(t0, t1, g=.8, bpm=150):
    b = 60 / bpm; t = t0; i = 0; f = hz('E2'); riff = [1, 1, 1.19, 1, 1.5, 1.33, 1.19, 1]
    while t < t1 - .02: m.kick(t, .45 * g) if i % 2 == 0 else m.snare(t, .25 * g); m.bass(f * riff[i % 8], t, b * .8, .2 * g); m.hat(t + b / 2, .06 * g); t += b; i += 1
def slide(t, f0, f1, d=.5, g=.3): tt = T(d); m.f(osc(glide(f0, f1, d), d) * env(len(tt), .01, .05), t, g, 0, .15)
def creak(t, d=.6, g=.25): cr = bp(osc(glide(220, 520, d, .5), d, 'saw'), 300, 2500) * (1 + .6 * np.sin(2 * np.pi * 23 * T(d))) * env(int(d * SR), .02, .1); m.f(cr, t, g, .2, .2)
def stamp(t): m.thump(t, .9); m.smack(t, .7); m.f(lp(noise(.25), 2500) * dec(.25, 18), t, .5)
def snap(t): m.f(hp(noise(.08), 1500) * dec(.08, 40), t, .9); m.boing(t + .02, .35, .4, 500, 120); m.f(hp(noise(.04), 3000) * dec(.04, 80), t + .03, .6)
def shutter(t): m.f(bp(noise(.03), 2000, 6000) * dec(.03, 90), t, .7); m.f(bp(noise(.05), 1200, 4000) * dec(.05, 60), t + .07, .5); m.sparkle(t + .05, .6, .15)
sneak(0, 16.5, .8); sneak(16.5, 20.5, .8)
# HOOK
for k in range(6): m.footstep(.05 + k * .14, .3, .4)
m.vo('ronaldo', 'siu', .15, .7, .3); m.whoosh(.6, .4, .3, False, .4); stamp(.95); m.vo('ronaldo', 'oof', 1.0, .8, .3)
m.xylo_rise(1.7, .15); m.whoosh(2.05, .3, .25, False, -.4); stamp(2.3); m.vo('kane', 'oof', 2.35, .8, -.3); m.vo('messi', 'laugh', 1.3, .5, 0, 'snicker', .6); m.crowd(2.5, 'laugh', 1.2, .25)
# DISGUISE
t = 3.0; m.pop(t + .1, .3, 700); m.tick(t + 1.0, True, .3); m.tick(t + 1.2, False, .3); creak(t + 1.8, 1.0, .3); snap(t + 2.9)
m.vo('ronaldo', 'cry', t + 3.1, .7, .1, 'wail', 1.2); m.vo('kane', 'laugh', t + 3.0, .6, -.4, 'point'); m.vo('messi', 'laugh', t + 3.4, .5, -.2, 'giggle', .8)
# FLICK
t = 8.0; m.choir([hz('D4'), hz('F#4'), hz('A4')], t + .1, 1.0, .1); m.cowbell(t + .3, .2); m.squeak(t + 2.0, .5); m.whip(t + 2.02, .35, .3); m.vo('kane', 'yelp', t + 2.05, .7, .3)
m.slide_whistle(t + 2.6, False, .6, .2, .3); m.clang(t + 3.2, .45, .3); m.thump(t + 3.2, .6); m.vo('kane', 'cry', t + 3.4, .7, .3, 'blubber', 1.0); m.vo('haaland', 'laugh', t + 2.3, .7, -.4, 'belly', 1.0)
# LADDER
t = 12.5; creak(t + .2, .5, .2); m.whoosh(t + 1.1, .7, .5, True, 0); m.f(hp(noise(.7), 800) * env(int(.7 * SR), .1, .3), t + 1.15, .3); creak(t + 1.6, .8, .35)
m.thump(t + 2.35, .9); m.crash(t + 2.38, .4); m.clang(t + 2.4, .35); m.f(lp(noise(.4), 1200) * dec(.4, 10), t + 2.36, .6); m.vo('ronaldo', 'ow', t + 2.4, .7, -.3); m.vo('kane', 'oof', t + 2.45, .7, .3); m.vo('mbappe', 'laugh', t + 2.9, .6, .3, 'giggle', .8)
# BALL
t = 16.5
for k in range(10): m.footstep(t + .1 + k * .13, .2, -.3)
m.honk(t + .4, .2); m.thwack(t + 1.6, .9); m.vo('ronaldo', 'yelp', t + 1.62, .6); m.vo('kane', 'yelp', t + 1.66, .6); m.crowd(t + 1.7, 'cheer', 1.4, .3); m.slide_whistle(t + 1.7, True, .8, .3, -.2); m.sparkle(t + 2.6, .8, .2)
m.vo('yamal', 'laugh', t + 2.2, .6, 0, 'point')
# CRY
t = 20.5; m.thump(t, .5); m.vo('ronaldo', 'cry', t + .2, .7, -.3, 'sob', 1.8); m.vo('kane', 'cry', t + .5, .6, .3, 'whimper', 1.6); m.crowd(t + .4, 'laugh', 2.0, .4)
# FLASH: idea → toss → bicycle → bowling → countdown → shutter
t = 23.0; m.cork(t + .05, .4); m.xylo_rise(t + .1, .12); m.oompah(t + .5, t + 3.0, ('C2', 'G1'), 140, .7); m.timpani(t + 3.0, 80, .5, roll=1.5)
m.whoosh(t + .6, .5, .25, True, .2); m.vo('ronaldo', 'siu', t + 1.0, .6, -.2); m.thwack(t + 1.2, .9)
for i, (h, who) in enumerate(zip((1.7, 2.0, 2.3, 2.6), ('haaland', 'messi', 'mbappe', 'yamal'))): m.smack(t + h, .8, (-1) ** i * .3); m.xylo(t + h + .02, [['C5', 'E5', 'G5', 'C6'][i]], .05, .2); m.vo(who, 'oof', t + h + .02, .6, (-1) ** i * .3)
m.crash(t + 2.65, .5); m.crowd(t + 2.7, 'gasp', 1.0, .3)
for i in range(3): m.tick(t + 3.0 + i * .5, True, .5)
m.whoosh(t + 3.6, .5, .3, True, 0); m.vo('ronaldo', 'siu', t + 4.0, .7, -.2); m.vo('kane', 'yay', t + 4.05, .6, .2); shutter(t + 4.6); m.f(hp(noise(.6), 3000) * dec(.6, 6), t + 4.6, .2)
# PHOTO
t = 30.0; m.whoosh(t, .6, .3, True, 0); m.choir([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t + .4, 2.0, .12); m.vo('ronaldo', 'laugh', t + 1.0, .5, -.2, 'cackle'); m.vo('kane', 'laugh', t + 1.2, .5, .2, 'belly', 1.0)
m.cork(t + 1.4, .4); m.kazoo(t + 3.0, ['C5', 'G4', 'C5'], .18, .15)
m.write(sys.argv[1])
