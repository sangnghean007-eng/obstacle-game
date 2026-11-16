"""Ep15 DON'T MESS WITH CR7 sound: swagger beat, fighting-game combo hits, cartoon cries, western showdown. No TTS.
hook 0 · mock 3.4 · combo 9.4 · cry 24.4 · rodri 29.4 · showdown 35.4 · twist 45.4 · end 50.4"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
END = 50.4; m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def beat(t0, t1, g=.8, bpm=92):
    b = 60 / bpm; t = t0; i = 0
    while t < t1 - .02: k808(t, .6 * g) if i % 4 in (0, 3) else None; m.snare(t, .25 * g) if i % 4 == 2 else None; m.hat(t + b / 2, .06 * g); t += b; i += 1
def fight(t0, t1, g=.8, bpm=150):
    b = 60 / bpm; t = t0; i = 0; f = hz('E2'); riff = [1, 1, 1.19, 1, 1.5, 1.33, 1.19, 1]
    while t < t1 - .02: m.kick(t, .45 * g) if i % 2 == 0 else m.snare(t, .25 * g); m.bass(f * riff[i % 8], t, b * .8, .2 * g); m.hat(t + b / 2, .06 * g); t += b; i += 1
def slide(t, f0, f1, d=.5, g=.3): tt = T(d); m.f(osc(glide(f0, f1, d), d) * env(len(tt), .01, .05), t, g, 0, .15)
def hit(t, n, g=.8): m.bonk(t, g); m.ding(t + .02, 880 * 2 ** (min(n, 13) / 12), .22, (-1) ** n * .3); m.f(hp(noise(.05), 2000) * dec(.05, 60), t, .4)
def creak(t, d=.6, g=.25): cr = bp(osc(glide(220, 520, d, .5), d, 'saw'), 300, 2500) * (1 + .6 * np.sin(2 * np.pi * 23 * T(d))) * env(int(d * SR), .02, .1); m.f(cr, t, g, .2, .2)
def whistle_tune(t0, notes, step=.36, g=.13):
    for i, n in enumerate(notes):
        if n: d = step * .9; tt = T(d); m.m(osc(hz(n) * (1 + .012 * np.sin(2 * np.pi * 6 * tt)), d) * env(len(tt), .03, .1), t0 + i * step, g, .2, .6)
# HOOK: swagger beat, BONK, shades fly
beat(0, 3.4, .8)
for k in range(5): m.footstep(.1 + k * .22, .25, -.3)
m.bonk(1.2, .9); m.boing(1.25, .3, .4, 300, 150); m.whoosh(1.3, .4, .2, True, -.4); m.f(m.wav('ooh_crowd'), 1.4, .25, 0, .3)
# MOCK: phone pop, Messi glory sting, Yamal laughs, CR7 steams
t = 3.4; beat(t, t + 6.0, .6); m.pop(t + .2, .4, 900); m.choir([hz('D4'), hz('F#4'), hz('A4')], t + .4, 1.4, .08); m.ding(t + .6, 1568, .2)
m.f(m.wav('laugh_m'), t + 3.0, .5, -.2, .2); m.f(m.wav('laugh_crowd'), t + 3.4, .3, 0, .3); m.f(m.wav('grumble_angry'), t + 2.6, .35, .3, .2)
m.f(hp(noise(1.2), 2500) * env(int(1.2 * SR), .1, .3), t + 2.7, .2, .4)
# COMBO: trunk, fighting-game music, 13 hits with rising dings, SIUUU
t = 9.4; creak(t + .2); m.sparkle(t + .4, 1.0, .15); fight(t + .6, t + 12.8, .8)
for n, tt_ in enumerate([1.41, 3.76, 4.56, 6.87, 7.27, 7.67, 8.07, 8.47]): m.whoosh(t + tt_ - .3, .3, .25, True, .3); hit(t + tt_, n + 1)
for i in range(5): m.whoosh(t + 10.4 + i * .35, .3, .15, False); hit(t + 10.95 + i * .35, 9 + i, .7)
m.f(m.wav('ooh_crowd'), t + 5.0, .25, 0, .3); m.f(m.wav('laugh_crowd'), t + 9.0, .3, 0, .3); m.f(m.wav('siu'), t + 12.8, .9, .2, .25); m.crash(t + 12.8, .4)
# CRY: wail, run, trip, SIUUU
t = 24.4; m.f(m.wav('wail'), t + .2, .5, -.2, .2)
for k in range(14): m.footstep(t + 1.6 + k * .1, .2, -.4)
m.thud(t + 2.45, .5); m.f(m.wav('laugh_crowd'), t + 2.6, .25, 0, .3)
# RODRI: sobbing, sigh, knuckle crack, cart, reveal
t = 29.4; m.f(m.wav('wail'), t + .2, .35, -.2, .2); m.f(m.wav('grumble_sad'), t + 2.0, .3, .2, .2)
for k in range(4): m.f(bp(noise(.03), 1500, 5000) * dec(.03, 80), t + 2.4 + k * .08, .5)
creak(t + 3.2, 1.6, .2); m.f(lp(noise(1.6), 300) * .5, t + 3.2, .3); m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4')], t + 3.6, 1.0, .35); m.choir([hz('D4'), hz('F#4'), hz('A4'), hz('D5')], t + 3.7, 1.8, .1); k808(t + 4.6, .9)
# SHOWDOWN: western whistle, tumbleweed, THOOM, climb + slide, wink, gasp
t = 35.4; whistle_tune(t + .1, ['A5', 'D6', 'A5', 'D6', 'A5', None, 'F5', 'G5', 'D5', None, None, None, 'A5', 'D6', 'A5', 'D6', 'A5', None, 'G5', 'C6'], .3, .12)
m.whoosh(t + .5, .8, .15, True, -.4); m.f(lp(noise(2.2), 300) * .5, t, .3); k808(t + 2.4, 1.0); m.crash(t + 2.4, .6); m.f(lp(noise(1.0), 120) * dec(1.0, 3) * 2, t + 2.4, .7); m.f(m.wav('ooh_crowd'), t + 2.6, .3, 0, .3)
m.pop(t + 3.0, .3); m.pop(t + 3.6, .3, 1100); m.f(m.wav('chuckle'), t + 3.7, .25, -.3, .2)
for k in range(6): m.footstep(t + 4.6 + k * .2, .2, .3)
slide(t + 6.0, 1400, 300, .7, .3); m.thud(t + 6.6, .5); m.ding(t + 7.2, 2093, .3); m.sparkle(t + 7.25, .6, .15); m.f(m.wav('gasp'), t + 7.6, .4, .3, .2); m.f(m.wav('laugh_crowd'), t + 8.2, .3, 0, .3)
# TWIST: phone dial + ring, sting
t = 45.4
for k in range(4): m.f(osc(950 + k * 120, .08) * dec(.08, 20), t + .6 + k * .1, .25, .3)
for k in range(2): m.f((osc(440, .4) + osc(480, .4)) * .5 * env(int(.4 * SR), .01, .05), t + 1.1 + k * .6, .25, .3)
m.brass_hit([hz('D3'), hz('G#3'), hz('D4')], t + 1.6, .7, .3); m.f(m.wav('ooh_crowd'), t + 1.7, .3, 0, .3); m.ding(t + 2.4, 1318, .3)
m.write(sys.argv[1])
