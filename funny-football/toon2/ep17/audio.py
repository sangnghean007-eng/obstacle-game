"""Ep17 THE GRASS IS GREENER sound: French accordion-ish waltz (Paris) vs Spanish guitar strum (Madrid), jump fails, cannon BOOM, pretzel lasso, door SLAM, rain. No TTS.
hook 0 · tantrum 3 · madrid 6.5 · split25 9.5 · split26 15 · back 20.5 · end 26.5 · END 31"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
END = 31.0; m = Mix(END)
def waltz(t0, t1, g=.6, bpm=150, key='C'):
    b = 60 / bpm; t = t0; i = 0; mel = ['E4', 'G4', 'C5', 'B4', 'G4', 'E4', 'F4', 'A4', 'D5', 'C5', 'A4', 'F4']; bass = ['C3', 'G2', 'F2', 'G2']
    while t < t1 - .02:
        if i % 3 == 0: m.bass(hz(bass[(i // 6) % 4]), t, b * .9, .25 * g)
        else: m.organ_stab([hz('E4'), hz('G4')], t, .12, .05 * g)
        m.pluck(hz(mel[i % 12]), t, b * .9, .16 * g, .2); t += b; i += 1
def flamenco(t0, t1, g=.6, bpm=120):
    b = 60 / bpm; t = t0; i = 0; ch = [['E3', 'G#3', 'B3'], ['F3', 'A3', 'C4'], ['G3', 'B3', 'D4'], ['F3', 'A3', 'C4']]
    while t < t1 - .02:
        for k, n in enumerate(ch[(i // 2) % 4]): m.pluck(hz(n), t + k * .02, .4, .14 * g, -.2)
        if i % 2: m.clap(t, .2 * g)
        t += b / 2; i += 1
def creak(t, d=.6, g=.25): cr = bp(osc(glide(220, 520, d, .5), d, 'saw'), 300, 2500) * (1 + .6 * np.sin(2 * np.pi * 23 * T(d))) * env(int(d * SR), .02, .1); m.f(cr, t, g, .2, .2)
def sad_trombone(t, g=.25):
    for i, n in enumerate(['D4', 'C#4', 'C4', 'B3']): d = .4 if i < 3 else 1.0; tt = T(d); m.m(osc(hz(n) * (1 + .01 * np.sin(2 * np.pi * 5 * tt)), d, 'saw') * env(len(tt), .02, .1), t + i * .4, g, 0, .3)
# HOOK: 7 jumps, 7 misses
waltz(0, 6.5, .7)
for i in range(7): t = i * .42; m.boing(t + .02, .25, .3, 200, 500); m.whoosh(t + .2, .2, .15, True, (-1) ** i * .3); m.thud(t + .3, .35)
m.f(m.wav('grumble_angry'), 2.6, .35, 0, .2)
# TANTRUM
t = 3.0
for i in range(5): m.thud(t + i * .3, .4); m.f(lp(noise(.1), 600) * dec(.1, 30), t + i * .3, .3)
m.f(m.wav('grumble_angry'), t + .2, .4, 0, .2); m.whoosh(t + 1.4, .3, .25); m.thud(t + 1.45, .4); m.pop(t + 1.6, .3, 700); m.f(m.wav('wail'), t + 2.0, .2, -.4, .3)
for i in range(8): m.footstep(t + 2.4 + i * .13, .25, .3)
# MADRID
t = 6.5; flamenco(t, 9.5, .8); m.brass_hit([hz('E4'), hz('G#4'), hz('B4')], t + 1.0, .6, .2); m.sparkle(t + 1.1, .8, .15); m.f(m.wav('cheer_crowd'), t + .8, .25, 0, .3)
# SPLIT 2025
t = 9.5; m.f(m.wav('cheer_crowd'), t + .6, .3, -.3, .3); m.crash(t + .6, .25); m.choir([hz('C4'), hz('E4'), hz('G4')], t + .6, 1.4, .1)
for i in range(4): m.thud(t + 1.2 + i * .15, .25, .3)
m.f(lp(noise(.3), 500) * dec(.3, 8), t + 2.3, .4); m.thud(t + 2.6, 1.0); m.f(lp(noise(1.2), 900) * dec(1.2, 3), t + 2.6, .8); m.crash(t + 2.62, .5); m.f(m.wav('wail'), t + 3.0, .4, .3, .2); sad_trombone(t + 3.2, .2)
# SPLIT 2026
t = 15.0; m.f(m.wav('cheer_crowd'), t + .5, .3, -.3, .3); m.choir([hz('D4'), hz('F#4'), hz('A4')], t + .5, 1.2, .1); m.ding(t + .55, 1568, .2)
for i in range(6): m.footstep(t + 1.0 + i * .1, .25, .3)
m.whoosh(t + 2.0, .5, .3, True, .2); m.boing(t + 2.5, .4, .5, 300, 120); m.f(m.wav('chuckle'), t + 2.6, .4, .3, .2); creak(t + 2.6, .5, .25); m.whoosh(t + 3.2, .6, .35, False, -.2); m.thud(t + 3.8, .7); m.f(m.wav('wail'), t + 3.9, .4, -.2, .2)
# BACK
t = 20.5; waltz(t, t + 2.4, .5)
for i in range(8): m.footstep(t + i * .15, .2, .3)
m.f(m.wav('grumble_sad'), t + 1.0, .35, 0, .2); creak(t + 1.4, .4, .3); m.ding(t + 1.6, 1318, .25); m.f(m.wav('chuckle'), t + 2.0, .4, 0, .2)
m.thud(t + 2.4, 1.0); m.crash(t + 2.42, .45); m.bonk(t + 2.45, .7); m.f(m.wav('wail'), t + 2.8, .45, 0, .2); m.pop(t + 3.2, .35, 600); m.f(m.wav('laugh_crowd'), t + 2.7, .35, .3, .3); m.f(m.wav('laugh_m'), t + 3.5, .3, .3, .2)
# END: rain + sad waltz + party behind the window
t = 26.5; m.f(lp(noise(4.5), 3000) * env(int(4.5 * SR), .3, .5), t, .12, 0, .2); waltz(t, END, .45, 120); m.f(m.wav('wail'), t + .3, .35, -.3, .2); m.f(m.wav('laugh_crowd'), t + .6, .25, .4, .3); m.badumtss(t + 3.8, .4)
m.write(sys.argv[1])
