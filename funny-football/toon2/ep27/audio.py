"""Ep27 THE NEW GANG sound: menu synth + swagger trap for the new gang; each OG gets his own sting (samba whistle for Neymar, sly pizzicato for Messi, epic brass for Ronaldo); escalating beat-up foley; sad limp-away waltz while the OGs laugh. vox2/fx2 only."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('g0', 2.0), ('g1', 1.7), ('g2', 1.7), ('g3', 1.8), ('g4', 2.4), ('g5', 5.8), ('g6', 5.6), ('g7', 6.2), ('g9', 7.4), ('g8', 4.4)]
ST = {}; _t = 0
for n, d in SEGS: ST[n] = _t; _t += d
END = _t; m = Mix2(END, ep=27); at = lambda n, z: ST[n] + z
def trap(t0, t1, g=.6, bpm=140):
    b = 60 / bpm; t = t0; i = 0
    while t < t1 - .02:
        if i % 8 in (0, 3, 6): m.m(osc(glide(90, 38, .45, .3), .45) * dec(.45, 4), t, .5 * g)
        if i % 8 == 4: m.snare(t, .25 * g)
        m.hat(t, .04 * g); t += b / 2; i += 1
for n in ('A3', 'C4', 'E4', 'A4'): m.m(lp(osc(hz(n), 2.0, 'saw'), 1500) * env(int(2.0 * SR), .3, .4), 0, .05)
m.boom(.05, .4); m.f(osc(880, .1, 'sq') * env(int(.1 * SR), .005, .03), 1.05, .15); m.f(osc(1320, .12, 'sq') * env(int(.12 * SR), .005, .03), 1.15, .15)
trap(at('g1', 0), at('g5', .5), .8)
for n, w in (('g1', 'yamal'), ('g2', 'mbappe'), ('g3', 'haaland')): m.whoosh(at(n, 0), .6, .4, True, -.3); m.thump(at(n, .6), .4); m.vo(w, 'laugh', at(n, .8), .45, 0, 'snicker')
for i in range(5): m.footstep(at('g4', i * .48), .45, (-1) ** i * .3)
# NEYMAR (5.8): juggling, elastico spin, nutmeg splits, rainbow bonk, samba dance
z0 = 'g5'
for i in range(10): m.f(lp(noise(.05), 900) * dec(.05, 40), at(z0, .1 + i * .12), .3, .3)
m.vo('yamal', 'grunt', at(z0, .7), .5); m.vo('haaland', 'laugh', at(z0, .8), .45, -.4, 'point')
for i in range(6): m.whoosh(at(z0, 1.3 + i * .13), .12, .15, i % 2 == 0)
m.vo('yamal', 'yelp', at(z0, 1.6), .55); m.thump(at(z0, 2.2), .5); m.squeak(at(z0, 2.75), .5); m.f(hp(noise(.2), 2500) * env(int(.2 * SR), .01, .1), at(z0, 2.8), .4); m.vo('mbappe', 'ow', at(z0, 2.82), .6)
m.whoosh(at(z0, 3.4), .6, .3, True); m.bonk(at(z0, 3.95), .7); m.vo('haaland', 'oof', at(z0, 3.97), .5); m.thump(at(z0, 4.2), .6); m.clang(at(z0, 4.22), .25); m.crowd(at(z0, 4.3), 'laugh', 1.2, .3)
for i in range(8): m.cowbell(at(z0, 4.3 + i * .18), .12) if i % 2 == 0 else m.clap(at(z0, 4.3 + i * .18), .15)
m.f(osc(2600, .4) * env(int(.4 * SR), .01, .05), at(z0, 4.4), .2)
# MESSI (5.6): laugh at him, wrong-guy punch, timber, back-heel bonk, slurp
z0 = 'g6'; [m.vo(w, 'laugh', at(z0, .65 + i * .08), .45, -.4 + i * .3, 'point') for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
m.whoosh(at(z0, 1.45), .2, .3); m.smack(at(z0, 1.6), 1.0, .4); m.vo('mbappe', 'yelp', at(z0, 1.62), .55, .4); m.thump(at(z0, 1.95), .5)
m.f(lp(noise(.5), 600) * env(int(.5 * SR), .02, .1), at(z0, 2.0), .4); m.vo('yamal', 'oof', at(z0, 2.48), .5); m.f(osc(glide(300, 120, .4), .4, 'saw') * env(int(.4 * SR), .01, .1) * .3, at(z0, 2.55), .3); m.thump(at(z0, 2.85), .7); m.vo('haaland', 'ow', at(z0, 2.8), .55)
m.thwack(at(z0, 3.4), .5); m.bonk(at(z0, 3.55), .7); m.vo('mbappe', 'oof', at(z0, 3.57), .5); m.slurp(at(z0, 4.1), .8, .35); m.vo('messi', 'laugh', at(z0, 4.6), .4, 0, 'snicker')
# RONALDO (6.2): abs clangs, knuckleball ricochet, SIUUU launch, stars
z0 = 'g7'; m.brass_hit([hz('C3'), hz('G3'), hz('C4')], at(z0, .3), .9, .25)
for i, (a_, w) in enumerate(((0.98, 'yamal'), (1.33, 'mbappe'), (1.68, 'haaland'))): m.clang(at(z0, a_), .55, -.3 + i * .3); m.vo(w, 'ow', at(z0, a_ + .05), .5)
m.vo('ronaldo', 'laugh', at(z0, 1.85), .45, 0, 'belly', .6); m.thwack(at(z0, 2.3), .8)
for i, a_ in enumerate((2.53, 2.77, 3.0)): m.bonk(at(z0, a_), .65, -.3 + i * .3); m.xylo(at(z0, a_ + .02), [['C5', 'E5', 'G5'][i]], .05, .2)
[m.vo(w, 'grunt', at(z0, 3.3 + i * .06), .45) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.vo('ronaldo', 'siu', at(z0, 3.5), .8); m.boom(at(z0, 4.0), .9); m.f(lp(noise(1.2), 300) * dec(1.2, 3), at(z0, 4.0), .5)
[m.vo(w, 'cry', at(z0, 4.1 + i * .1), .45, -.4 + i * .3, 'wail', .7) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.slide_whistle(at(z0, 4.1), True, .9, .3); m.sparkle(at(z0, 4.9), 1.0, .25)
# FINAL (7.4): rage, clash, fly, combo, boom, launch, crash, K.O.
z0 = 'g9'; m.f(osc(glide(300, 120, .5), .5, 'sq') * env(int(.5 * SR), .01, .1), at(z0, .05), .2); m.boom(at(z0, .1), .35); [m.vo(w, 'grunt', at(z0, .4 + i * .1), .5) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
trap(at(z0, .9), at(z0, 4.6), 1.0, 170); m.timpani(at(z0, 1.0), 70, .4, roll=.6)
m.boom(at(z0, 1.7), 1.0); m.f(hp(noise(.5), 1500) * dec(.5, 5), at(z0, 1.7), .5); [m.vo(w, 'yelp', at(z0, 2.1 + i * .07), .5) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.thump(at(z0, 2.8), .5)
m.choir([hz('C3'), hz('G3'), hz('C4'), hz('E4')], at(z0, 2.8), 1.8, .22); m.thwack(at(z0, 2.85), .5); m.thwack(at(z0, 3.3), .6); m.vo('ronaldo', 'siu', at(z0, 3.7), .7); m.thwack(at(z0, 4.1), .9); m.f(lp(noise(.6), 2000) * env(int(.6 * SR), .05, .2), at(z0, 4.1), .4)
m.boom(at(z0, 4.55), 1.0); [m.vo(w, 'cry', at(z0, 4.65 + i * .08), .5, -.4 + i * .3, 'wail', .9) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.slide_whistle(at(z0, 4.7), True, .9, .35); m.sparkle(at(z0, 5.2), .6, .25)
m.slide_whistle(at(z0, 5.6), False, .4, .3); m.clang(at(z0, 5.95), .5); m.clang(at(z0, 6.0), .4, .4); m.thump(at(z0, 5.95), .8); m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], at(z0, 6.2), 1.0, .3); m.crowd(at(z0, 6.25), 'cheer', 1.4, .5)
# end: OGs laugh, sad waltz as the kids limp away
z0 = 'g8'; m.vo('ronaldo', 'laugh', at(z0, .2), .55, -.4, 'belly', 1.4); m.vo('neymar', 'laugh', at(z0, .4), .5, -.2, 'giggle', 1.2); m.vo('messi', 'laugh', at(z0, .6), .45, 0, 'snicker')
for i, n in enumerate(['A4', 'G#4', 'G4', 'F#4', 'F4']): m.kazoo(at(z0, .3 + i * .5), [n], .45, .1)
[m.vo(w, 'cry', at(z0, 1.0 + i * .3), .35, .4, 'whimper', 1.2) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
# outro bed to the very end (QA: no dead air)
m.vo('ronaldo', 'laugh', at(z0, 2.9), .4, -.4, 'point'); m.kazoo(at(z0, 2.8), ['E4'], 1.3, .1); m.m(lp(osc(hz('A2'), 1.6, 'saw'), 600) * env(int(1.6 * SR), .1, .8), at(z0, 2.8), .12)
print(round(END, 2)); m.write(sys.argv[1])
