"""Ep26 13 YEARS IN LINE sound: elevator/bossa 'waiting music' that slows and detunes as the years pass (new style), calendar flip whooshes,
door bell, heist funk for the new gen, epic choir when the OGs 'un-age', action hits for the payback, couch-gaming end. vox2/fx2 only."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('q13', 3.2), ('q16', 2.0), ('q18', 3.2), ('q22', 3.4), ('q23', 2.4), ('qop', 4.0), ('qri', 2.6), ('qpa', 5.0), ('qso', 3.6)]
ST = {}; _t = 0
for n, d in SEGS: ST[n] = _t; _t += d
END = _t; m = Mix2(END, ep=26); at = lambda n, z: ST[n] + z
def bossa(t0, t1, g=.5, bpm=120, det=0.0):
    b = 60 / bpm; t = t0; i = 0; ch = [['D4', 'F4', 'A4', 'C5'], ['G3', 'B3', 'D4', 'F4'], ['C4', 'E4', 'G4', 'B4'], ['A3', 'C#4', 'E4', 'G4']]; mel = ['A4', 'C5', 'E5', 'D5', 'B4', 'G4', 'A4', 'E4']
    while t < t1 - .02:
        k = (t - t0) / max(.1, t1 - t0); f = 1 - det * k
        if i % 2 == 0: [m.pluck(hz(n) * f, t + j * .01, .3, .06 * g, -.2) for j, n in enumerate(ch[(i // 4) % 4])]
        if i % 4 in (0, 3): m.bass(hz(['D2', 'G1', 'C2', 'A1'][(i // 4) % 4]) * f, t, b * .9, .2 * g)
        if i % 2: m.m(hp(noise(.05), 3000) * dec(.05, 50), t, .05 * g)
        if i % 2 == 0: m.xylo(t, [mel[(i // 2) % 8]], .05, .07 * g)
        t += b / 2; i += 1
bossa(0, at('qop', 0), .7, 116, .12)
for n in ('q16', 'q18', 'q22', 'q23'): m.f(hp(noise(.25), 1800) * env(int(.25 * SR), .01, .1), at(n, 0), .35)
for i in range(5): m.f(hp(noise(.15), 2000) * env(int(.15 * SR), .01, .05), at('q18', i * .64), .3)
# 2013 Neymar fake faint → chair
m.vo('neymar', 'cry', at('q13', 1.2), .5, 0, 'wail', .5); m.thump(at('q13', 1.3), .3); m.vo('ronaldo', 'hmm', at('q13', 1.6), .35); m.thump(at('q13', 2.2), .3); m.vo('neymar', 'laugh', at('q13', 2.4), .4, 0, 'snicker')
# 2016 Ronaldo zoom + Euro
m.whoosh(at('q16', .4), .3, .35); m.whoosh(at('q16', .85), .3, .35, False); m.brass_hit([hz('C4'), hz('E4'), hz('G4')], at('q16', .9), .5, .2); m.vo('ronaldo', 'siu', at('q16', 1.0), .5)
m.vo('ronaldo', 'hmm', at('q18', 1.0), .3); m.vo('messi', 'hmm', at('q18', 1.6), .3); m.vo('haaland', 'grunt', at('q18', 2.2), .35)
# 2022 Messi World Cup, Ronaldo push-ups
m.whoosh(at('q22', .3), .3, .35); m.choir([hz('D4'), hz('F#4'), hz('A4')], at('q22', .8), .9, .12); m.vo('messi', 'yay', at('q22', .9), .45)
for i in range(16): m.vo('ronaldo', 'grunt', at('q22', 1.4 + i * .12), .25 + .02 * i, .3)
# 2023 poof x3, crutches
for i in range(3): m.cork(at('q23', .4 + i * .05), .25)
m.vo('neymar', 'ow', at('q23', .9), .4)
# 2026 doors open: bell + heist funk
m.f(osc(1318, .6) * dec(.6, 5) + .5 * osc(1760, .6) * dec(.6, 6), at('qop', .2), .3); m.crowd(at('qop', .3), 'gasp', .8, .2)
b = 60 / 104; t = at('qop', .5); i = 0
while t < at('qri', 0): m.kick(t, .3) if i % 2 == 0 else m.clap(t, .15); m.bass(hz(['E2', 'G2', 'A2', 'G2'][i % 4]), t, b * .45, .2); m.hat(t + b / 2, .05); t += b / 2; i += 1
m.vo('haaland', 'grunt', at('qop', .95), .55); [m.vo(w, 'yelp', at('qop', 1.0 + j * .07), .4, -.3 + j * .3) for j, w in enumerate(('ronaldo', 'messi', 'neymar'))]; m.thump(at('qop', 1.9), .5)
m.whoosh(at('qop', 2.0), .5, .45, True, .4); m.f(lp(noise(.5), 1500) * env(int(.5 * SR), .05, .3), at('qop', 2.05), .3); m.cork(at('qop', 2.6), .35)
m.whoosh(at('qop', 2.9), .3, .3); m.f(lp(noise(1.0), 900) * env(int(SR), .05, .3), at('qop', 3.0), .2); m.vo('yamal', 'laugh', at('qop', 3.2), .5, 0, 'point')
# rise: choir + cardigans + crack
m.choir([hz('C3'), hz('G3'), hz('C4'), hz('E4')], at('qri', .4), 2.2, .22); m.timpani(at('qri', .1), 70, .45, roll=.6); m.f(hp(noise(.4), 2000) * dec(.4, 8), at('qri', .8), .5); m.boom(at('qri', .8), .4); m.brass_hit([hz('C3'), hz('G3'), hz('C4')], at('qri', 1.4), 1.0, .28)
for i in range(4): m.footstep(at('qri', 1.4 + i * .3), .45)
# payback
b = 60 / 150; t = at('qpa', 0); i = 0
while t < at('qpa', 3.9): m.kick(t, .4) if i % 2 == 0 else m.snare(t, .22); m.hat(t + b / 2, .05); t += b; i += 1
m.whoosh(at('qpa', .45), .3, .3); m.vo('neymar', 'cry', at('qpa', .55), .5, 0, 'wail', .5); m.thump(at('qpa', .75), .5); m.vo('yamal', 'yelp', at('qpa', .8), .55); m.slide_whistle(at('qpa', .8), True, .5, .25)
m.thwack(at('qpa', 1.3), .3); [m.f(lp(noise(.05), 900) * dec(.05, 40), at('qpa', 1.6 + j * .1), .4) for j in range(4)]; m.whoosh(at('qpa', 1.95), .3, .3); m.vo('mbappe', 'gasp', at('qpa', 2.0), .5)
m.vo('haaland', 'grunt', at('qpa', 2.5), .5); m.vo('ronaldo', 'grunt', at('qpa', 2.6), .5); m.thwack(at('qpa', 2.9), .7); m.thump(at('qpa', 3.3), .6)
m.vo('ronaldo', 'siu', at('qpa', 3.3), .8); m.crowd(at('qpa', 3.35), 'cheer', 1.6, .55); m.boom(at('qpa', 3.35), .4)
m.vo('yamal', 'cry', at('qpa', 3.9), .55, -.3, 'blubber', 1.0); m.vo('mbappe', 'cry', at('qpa', 4.05), .5, 0, 'sob', .9); m.vo('haaland', 'cry', at('qpa', 4.2), .5, .3, 'wail', .7)
# sofa: game beeps, Ronaldo shouting, laugh
for i in range(10): m.f(osc([660, 880, 990, 1320][i % 4], .08, 'sq') * env(int(.08 * SR), .005, .03), at('qso', .2 + i * .3), .08)
for i in range(4): m.vo('ronaldo', 'siu' if i % 2 else 'yelp', at('qso', .3 + i * .7), .45)
m.vo('messi', 'laugh', at('qso', 1.6), .4, .3, 'snicker'); m.kazoo(at('qso', 2.6), ['C5', 'E5', 'G5', 'C6'], .14, .12)
print(round(END, 2)); m.write(sys.argv[1])
