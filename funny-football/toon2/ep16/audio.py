"""Ep16 THE TEAM PHOTO sound: sneaky heist beat, stamps, slingshot snap, flick, ladder crash, golazo, bowling strike, shutter. No TTS.
hook 0 · disguise 3 · flick 8 · ladder 12.5 · ball 16.5 · cry 20.5 · flash 23 · photo 30 · end 36"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
OLD = [(0, 3), (3, 5), (8, 4.5), (12.5, 4), (16.5, 4), (20.5, 2.5), (23, 7), (30, 6)]
NEWD = [3, 5, 4.5, 4, 3, 2.5, 5.4, 4.5]
NEW0 = [sum(NEWD[:i]) for i in range(len(NEWD))]
def R(t):
    for (a_, d_), n0 in zip(OLD, NEW0):
        if t < a_ + d_: return n0 + (t - a_)
    return NEW0[-1] + (t - OLD[-1][0])
END = sum(NEWD); m = Mix(END)
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
def stamp(t): m.thud(t, .9); m.bonk(t, .6); m.f(lp(noise(.25), 2500) * dec(.25, 18), t, .5)
def snap(t): m.f(hp(noise(.08), 1500) * dec(.08, 40), t, .9); m.boing(t + .02, .35, .4, 500, 120); m.f(hp(noise(.04), 3000) * dec(.04, 80), t + .03, .6)
def shutter(t): m.f(bp(noise(.03), 2000, 6000) * dec(.03, 90), t, .7); m.f(bp(noise(.05), 1200, 4000) * dec(.05, 60), t + .07, .5); m.sparkle(t + .05, .6, .15)
sneak(0, 16.5, .8); sneak(16.5, 20.5, .8)
# HOOK
for k in range(6): m.footstep(.05 + k * .14, .3, .4)
m.f(m.wav('siu'), .15, .45, .3, .1); m.whoosh(.6, .4, .3, False, .4); stamp(.95); m.f(m.wav('wail'), 1.1, .3, .3, .2)
m.ding(1.75, 1568, .25); m.whoosh(2.05, .3, .25, False, -.4); stamp(2.3); m.f(m.wav('chuckle'), 1.3, .4, 0, .2); m.f(m.wav('laugh_crowd'), 2.5, .25, 0, .3)
# DISGUISE
t = 3.0; m.pop(t + .1, .3, 700); m.tick(t + 1.0, True, .3); m.tick(t + 1.2, False, .3); creak(t + 1.8, 1.0, .3); snap(t + 2.9)
m.f(m.wav('wail'), t + 3.1, .45, .1, .2); m.f(m.wav('laugh_m'), t + 3.0, .4, -.4, .2); m.f(m.wav('chuckle'), t + 3.3, .35, -.2, .2)
# FLICK
t = 8.0; m.choir([hz('D4'), hz('F#4'), hz('A4')], t + .1, 1.0, .1); m.ding(t + .3, 1318, .2); m.pop(t + 2.0, .6, 1400); m.whoosh(t + 2.02, .5, .35, True, .3)
m.whoosh(t + 2.6, .6, .2, False, .3); m.bonk(t + 3.2, .9, .3); m.ding(t + 3.22, 988, .25); m.f(m.wav('wail'), t + 3.4, .45, .3, .2); m.f(m.wav('chuckle'), t + 2.3, .4, -.4, .2)
# LADDER
t = 12.5; creak(t + .2, .5, .2); m.whoosh(t + 1.1, .7, .5, True, 0); m.f(hp(noise(.7), 800) * env(int(.7 * SR), .1, .3), t + 1.15, .3); creak(t + 1.6, .8, .35)
m.thud(t + 2.35, .9); m.crash(t + 2.38, .4); m.bonk(t + 2.4, .6); m.f(lp(noise(.4), 1200) * dec(.4, 10), t + 2.36, .6); m.f(m.wav('wail'), t + 2.6, .45, -.3, .2); m.f(m.wav('chuckle'), t + 2.9, .35, .3, .2)
# BALL
t = 16.5
for k in range(10): m.footstep(t + .1 + k * .13, .2, -.3)
m.boing(t + .4, .2, .4, 160, 260); m.thwack(t + 1.6, .9); m.cheer_burst(t + 1.7, .3); m.whoosh(t + 1.7, .8, .3, True, -.2); m.sparkle(t + 2.6, .8, .2); m.ding(t + 2.7, 2093, .2)
m.f(m.wav('laugh_crowd'), t + 2.2, .3, 0, .3)
# CRY
t = 20.5; m.thud(t, .5); m.f(m.wav('wail'), t + .2, .45, -.3, .2); m.f(m.wav('wail'), t + .5, .4, .3, .2); m.f(m.wav('laugh_crowd'), t + .4, .4, 0, .3); m.f(m.wav('laugh_m'), t + 1.2, .3, .3, .2)
# FLASH: idea → toss → bicycle → bowling → countdown → shutter
t = 23.0; m.pop(t + .05, .4, 1200); m.ding(t + .1, 2093, .25); fight(t + .5, t + 4.6, .7)
m.whoosh(t + .6, .5, .25, True, .2); m.f(m.wav('siu'), t + 1.1, .4, -.2, .1); m.thwack(t + 1.2, .9)
for i, h in enumerate((1.7, 2.0, 2.3, 2.6)): m.bonk(t + h, .8, (-1) ** i * .3); m.ding(t + h + .02, 880 * 2 ** (i * 4 / 12), .22)
m.crash(t + 2.65, .5); m.f(m.wav('ooh_crowd'), t + 2.7, .35, 0, .3)
for i in range(3): m.tick(t + 3.0 + i * .5, True, .5); m.ding(t + 3.0 + i * .5, 880, .12)
m.whoosh(t + 3.6, .5, .3, True, 0); m.f(m.wav('siu_crowd'), t + 4.0, .4, 0, .2); shutter(t + 4.6); m.f(hp(noise(.6), 3000) * dec(.6, 6), t + 4.6, .2)
# PHOTO
t = 30.0; m.whoosh(t, .6, .3, True, 0); m.choir([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t + .4, 2.0, .12); m.f(m.wav('laugh_crowd'), t + 1.0, .3, 0, .3)
m.pop(t + 1.4, .4, 900); m.ding(t + 2.2, 1318, .2); m.badumtss(t + 3.6, .4)
m.write(sys.argv[1])
