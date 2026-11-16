"""Ep15 DON'T MESS WITH CR7 sound: swagger beat, fighting-game combo hits, cartoon cries, western showdown. No TTS.
hook 0 · mock 3.4 · combo 9.4 · cry 24.4 · rodri 29.4 · showdown 35.4 · twist 45.4 · end 50.4"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
OLD = [(0, 3.4, .8), (3.4, 6.0, .65), (9.4, 15.0, 14 / 15), (24.4, 5.0, .6), (29.4, 6.0, .65), (35.4, 10.0, .75), (45.4, 5.0, .7)]
NEW0 = []; _t = 0
for a_, d_, sl_ in OLD: NEW0.append(_t); _t += d_ * sl_
def R(t):
    for (a_, d_, sl_), n0 in zip(OLD, NEW0):
        if t < a_ + d_ or (a_, d_, sl_) == OLD[-1]: return n0 + (t - a_) * sl_
END = _t; m = Mix(END)
_put = m.put; m.put = lambda bus, s, t0, *a, **k: _put(bus, s, R(t0), *a, **k)
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
# COMBO v2 (placed in NEW time, see bottom)
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
# ---- COMBO v2 sounds, placed directly at new times ----
m.put = _put; C0 = NEW0[2]
fight(C0 + .4, C0 + 12.4, .8); creak(C0 + .1)
m.whoosh(C0 + .8, .3, .3, True); m.thwack(C0 + 1.0, 1.0); slide(C0 + 1.05, 400, 2000, .8, .3); m.f(m.wav('ooh_crowd'), C0 + 1.2, .3, 0, .3); slide(C0 + 1.6, 2000, 300, .4, .25); m.thud(C0 + 1.95, .8); m.f(bp(noise(.3), 100, 800) * dec(.3, 8), C0 + 1.95, .6); m.f(m.wav('laugh_crowd'), C0 + 2.2, .3, 0, .3)
x = sum(a_ * osc(f_, .9) for f_, a_ in [(420, 1), (1013, .7), (1730, .5), (2600, .4)]) * dec(.9, 4); m.f(x + hp(noise(.9), 3000) * dec(.9, 5) * .6, C0 + 3.8, .7); m.boing(C0 + 4.6, .4, .5, 150, 600); m.f(m.wav('chuckle'), C0 + 4.2, .3, .3, .2)
m.f(lp(noise(.5), 400) * dec(.5, 6), C0 + 5.7, .4)
for k_, s_ in enumerate([6.0, 6.4, 6.8, 7.2, 7.6]): k808(C0 + s_, .7); m.whoosh(C0 + s_, .3, .25, False, -.3)
for s_ in (6.2, 6.6, 7.0): m.whoosh(C0 + s_, .25, .2, True, .4)
m.bonk(C0 + 7.3, .7); m.bonk(C0 + 7.7, .9); slide(C0 + 7.95, 900, 300, .35, .25); m.thud(C0 + 8.3, .9); m.f(bp(noise(.4), 200, 2000) * dec(.4, 8), C0 + 8.3, .5); m.f(m.wav('laugh_crowd'), C0 + 8.4, .3, 0, .3)
for k_ in range(10): m.hat(C0 + 9.0 + k_ * .12, .1)
for k_ in range(12): m.ding(C0 + 10.4 + k_ * .13, 1568 + (k_ % 5) * 220, .2, (-1) ** k_ * .4); m.pop(C0 + 10.45 + k_ * .13, .2, 1200)
m.f(m.wav('siu'), C0 + 12.5, 1.0, 0, .25); k808(C0 + 12.5, 1.0); m.crash(C0 + 12.5, .6); m.whoosh(C0 + 12.6, .8, .4, False, -.5); m.brass_hit([hz('E3'), hz('B3'), hz('E4'), hz('G#4')], C0 + 12.9, 1.0, .4); m.cheer_burst(C0 + 12.9, .4)
m.write(sys.argv[1])
