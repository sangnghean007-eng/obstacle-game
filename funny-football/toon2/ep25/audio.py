"""Ep25 v2 sound: loading-screen synth pad, synthwave trailer for the new gen (original), record scratch at the bump, choir + brass for the OGs,
character-switch whooshes, Ronaldo SIUUU shockwave, Messi bonk-bonk-bonk, Neymar scream + rolling boulder + whistle, MISSION FAILED sting. vox2/fx2 only."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('ld', 2.4), ('ya', 2.2), ('mb', 2.0), ('ha', 2.0), ('wk', 2.6), ('bp', 1.2), ('rv', 2.0), ('sr', 1.8), ('sm', 1.8), ('sn', 2.4), ('en', 3.0)]
ST = {}; _t = 0
for n, d in SEGS: ST[n] = _t; _t += d
END = _t; m = Mix2(END, ep=252); at = lambda n, z: ST[n] + z
def synthwave(t0, t1, g=.7, bpm=100):
    b = 60 / bpm; t = t0; i = 0; arp = ['A3', 'C4', 'E4', 'A4', 'F3', 'A3', 'C4', 'F4', 'C4', 'E4', 'G4', 'C5', 'G3', 'B3', 'D4', 'G4']; bass = ['A1', 'F1', 'C2', 'G1']
    while t < t1 - .02:
        n = arp[i % 16]; d = b / 4; m.m(lp(osc(hz(n), d * .9, 'saw'), 2600) * env(int(d * .9 * SR), .005, .05), t, .07 * g, .3 if i % 2 else -.3, .25)
        if i % 4 == 0: m.m(lp(osc(hz(bass[(i // 16) % 4]), b, 'saw'), 500) * env(int(b * SR), .01, .1), t, .22 * g)
        if i % 8 == 0: m.kick(t, .4 * g)
        if i % 8 == 4: m.snare(t, .3 * g); m.f(hp(noise(.3), 1500) * dec(.3, 6), t, .1 * g)
        t += d; i += 1
for n in ('A3', 'C4', 'E4'): m.m(lp(osc(hz(n), 2.4, 'saw'), 1200) * env(int(2.4 * SR), .8, .4), 0, .06)
for i in range(3): m.tick(.4 + i * .8, True, .2)
synthwave(at('ya', 0), at('bp', .5), .8)
# Yamal: scooter, NO BRAKES, crash into bins
m.whoosh(at('ya', 0), .6, .35, True, -.4); m.vo('yamal', 'yelp', at('ya', .65), .5); m.boom(at('ya', .9), .4); m.clang(at('ya', .92), .4); m.clang(at('ya', 1.0), .3, .4); m.crowd(at('ya', 1.1), 'laugh', 1.0, .3); m.vo('yamal', 'hmph', at('ya', 1.7), .45)
# Mbappé: cups fall off, empty bag
m.whoosh(at('mb', 0), .6, .4, True, .4); [m.clang(at('mb', .2 + i * .15), .25, .3) for i in range(4)]; m.vo('mbappe', 'gasp', at('mb', 1.2), .5); m.wahwah(at('mb', 1.25), .18)
# Haaland: lift, car alarm, yeet
m.vo('haaland', 'grunt', at('ha', .2), .6)
for i in range(9): m.f(osc(900 if i % 2 else 650, .1, 'sq') * env(int(.1 * SR), .005, .02), at('ha', .6 + i * .1), .12)
m.whoosh(at('ha', 1.3), .5, .4, True, .5); m.vo('haaland', 'laugh', at('ha', 1.4), .5, 0, 'belly', .6); m.boom(at('ha', 1.9), .2)
for i in range(5): m.footstep(at('wk', i * .5), .5, (-1) ** i * .3)
m.f(osc(glide(200, 1200, 2.2), 2.2, 'saw') * env(int(2.2 * SR), 1.8, .2) * .25, at('wk', .3), .2)
m.thump(at('bp', .5), 1.0); m.smack(at('bp', .5), .7); m.scratch(at('bp', .52), .55); [m.vo(w, 'oof', at('bp', .55 + i * .05), .5, -.4 + i * .4) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
m.choir([hz('C4'), hz('E4'), hz('G4'), hz('C5')], at('rv', .3), 1.7, .2); m.timpani(at('rv', .1), 70, .5, roll=.7); m.brass_hit([hz('C3'), hz('G3'), hz('C4'), hz('E4')], at('rv', .9), 1.0, .3)
for n in ('sr', 'sm', 'sn'): m.whoosh(at(n, .05), .25, .3); m.f(osc(glide(500, 1200, .12), .12) * dec(.12, 20), at(n, .3), .2)
m.vo('ronaldo', 'siu', at('sr', .45), .8); m.boom(at('sr', 1.0), .7); m.f(lp(noise(1.0), 300) * dec(1.0, 3), at('sr', 1.0), .5); [m.vo(w, 'yelp', at('sr', 1.05 + i * .05), .4, -.4 + i * .4) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
[m.f(lp(noise(.04), 800) * dec(.04, 40), at('sm', i * .08), .3) for i in range(7)]
for i in range(3): m.bonk(at('sm', .9 + i * .3), .55, -.3 + i * .3); m.xylo(at('sm', .92 + i * .3), [['C5', 'E5', 'G5'][i]], .05, .2)
m.vo('messi', 'laugh', at('sm', 1.6), .4, .3, 'snicker')
m.pop(at('sn', .6), .25, 1400); m.vo('neymar', 'cry', at('sn', .7), .7, 0, 'wail', .9); m.f(lp(noise(1.2), 220) * env(int(1.2 * SR), .1, .2) * (1 + .5 * np.sin(2 * np.pi * 6 * T(1.2))), at('sn', .9), .6)
for i, w in enumerate(('haaland', 'mbappe', 'yamal')): m.smack(at('sn', 1.2 + i * .15), .6); m.vo(w, 'oof', at('sn', 1.22 + i * .15), .45)
tt = T(.4); m.f(osc(2800 * (1 + .03 * np.sin(2 * np.pi * 40 * tt)), .4) * env(len(tt), .01, .03), at('sn', 1.65), .35)
m.f(osc(glide(400, 120, 1.0), 1.0, 'saw') * env(int(SR), .01, .2) * .4, at('en', .4), .3); m.boom(at('en', .4), .4); m.vo('ronaldo', 'laugh', at('en', .6), .55, -.3, 'belly', 1.2); m.vo('messi', 'laugh', at('en', .8), .5, .3, 'snicker'); m.vo('neymar', 'laugh', at('en', 1.0), .5, 0, 'giggle', 1.0)
for i in range(6): m.footstep(at('en', i * .1), .3, (-1) ** i * .6)
print(round(END, 2)); m.write(sys.argv[1])
