"""Ep27 THE NEW GANG sound: menu synth + swagger trap for the new gang; each OG gets his own sting (samba whistle for Neymar, sly pizzicato for Messi, epic brass for Ronaldo); escalating beat-up foley; sad limp-away waltz while the OGs laugh. vox2/fx2 only."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('g0', 2.0), ('g1', 1.7), ('g2', 1.7), ('g3', 1.8), ('g4', 2.4), ('g5', 4.6), ('g6', 4.6), ('g7', 4.8), ('g9', 7.2), ('g8', 4.4)]
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
# Neymar
z0 = 'g5'; m.thump(at(z0, .5), .8); m.scratch(at(z0, .52), .45); [m.vo(w, 'oof', at(z0, .55 + i * .05), .4, -.3 + i * .3) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
for i in range(6): m.f(osc(2600 + (i % 2) * 300, .12) * env(int(.12 * SR), .005, .03), at(z0, .6 + i * .12), .12)
[m.vo(w, 'grunt', at(z0, 1.0 + i * .1), .45) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.vo('neymar', 'laugh', at(z0, 1.3), .45, .4, 'giggle', .8)
for i in range(8): m.f(lp(noise(.05), 900) * dec(.05, 40), at(z0, 1.7 + i * .1), .35, .3)
m.whoosh(at(z0, 1.8), .8, .3, True); m.boom(at(z0, 2.6), .5); m.clang(at(z0, 2.62), .3); [m.vo(w, 'ow', at(z0, 2.65 + i * .08), .45) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.thump(at(z0, 3.0), .6); m.crowd(at(z0, 3.0), 'laugh', 1.3, .3)
# Messi
z0 = 'g6'; [m.pluck(hz(n), at(z0, .1 + i * .15), .12, .12) for i, n in enumerate(['E5', 'G5', 'E5', 'C5'])]
for w, d in (('yamal', 0), ('mbappe', .1), ('haaland', .2)): m.vo(w, 'laugh', at(z0, .85 + d), .45, 0, 'point')
for i in range(6): m.footstep(at(z0, 1.7 + i * .1), .35, .2)
m.thwack(at(z0, 2.2), .6); [(m.bonk(at(z0, h), .7, -.3 + i * .3), m.xylo(at(z0, h + .02), [['C5', 'E5', 'G5'][i]], .05, .2)) for i, h in enumerate((2.35, 2.55, 2.75))]
[m.vo(w, 'yelp', at(z0, h + .03), .45) for w, h in (('yamal', 2.35), ('mbappe', 2.55), ('haaland', 2.75))]; m.vo('messi', 'laugh', at(z0, 3.1), .4, .4, 'snicker'); m.crowd(at(z0, 3.2), 'laugh', 1.2, .3)
# Ronaldo
z0 = 'g7'; m.brass_hit([hz('C3'), hz('G3'), hz('C4')], at(z0, .3), 1.0, .28); m.timpani(at(z0, .6), 70, .3, roll=.6)
[m.vo(w, 'gasp', at(z0, .8 + i * .1), .4) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; [m.squeak(at(z0, .9 + i * .12), .2) for i in range(5)]
[m.vo(w, 'grunt', at(z0, 1.6 + i * .06), .45) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.whoosh(at(z0, 1.9), .5, .35, True)
m.vo('ronaldo', 'siu', at(z0, 2.0), .8); m.boom(at(z0, 2.45), .9); m.f(lp(noise(1.2), 300) * dec(1.2, 3), at(z0, 2.45), .55)
[m.vo(w, 'cry', at(z0, 2.55 + i * .1), .45, -.4 + i * .3, 'wail', .6) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]; m.thump(at(z0, 3.05), .6); m.crowd(at(z0, 3.1), 'cheer', 1.4, .45)
# FINAL 3 vs 3
z0 = 'g9'; m.f(osc(glide(300, 120, .5), .5, 'sq') * env(int(.5 * SR), .01, .1), at(z0, .05), .2); m.boom(at(z0, .1), .4); m.vo('generic_m', 'yay', at(z0, .5), .5)
trap(at(z0, .8), at(z0, 6.2), 1.0, 160)
m.vo('yamal', 'grunt', at(z0, 1.0), .5); m.vo('neymar', 'cry', at(z0, 1.3), .6, 0, 'wail', .5); m.whoosh(at(z0, 1.45), .4, .3); m.thump(at(z0, 1.9), .6); m.vo('yamal', 'oof', at(z0, 1.9), .5)
m.whoosh(at(z0, 2.1), .5, .4, True, .5); m.clang(at(z0, 2.6), .6, .6); m.vo('mbappe', 'ow', at(z0, 2.62), .55); m.vo('messi', 'laugh', at(z0, 2.8), .4, 0, 'snicker')
for i in range(4): m.footstep(at(z0, 3.3 + i * .1), .5)
m.spring(at(z0, 3.72), .5, .8); m.vo('haaland', 'yelp', at(z0, 3.8), .55); m.vo('ronaldo', 'laugh', at(z0, 4.0), .45, .3, 'belly', .6)
m.thwack(at(z0, 4.5), .5); m.thwack(at(z0, 4.95), .5); m.vo('ronaldo', 'siu', at(z0, 5.2), .7); m.thwack(at(z0, 5.3), .9)
m.boom(at(z0, 5.6), .7); [m.smack(at(z0, 5.6 + i * .04), .6) for i in range(3)]; m.crowd(at(z0, 5.65), 'cheer', 1.8, .55)
m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], at(z0, 6.2), 1.0, .3); m.boom(at(z0, 6.2), .4)
# end: OGs laugh, sad waltz as the kids limp away
z0 = 'g8'; m.vo('ronaldo', 'laugh', at(z0, .2), .55, -.4, 'belly', 1.4); m.vo('neymar', 'laugh', at(z0, .4), .5, -.2, 'giggle', 1.2); m.vo('messi', 'laugh', at(z0, .6), .45, 0, 'snicker')
for i, n in enumerate(['A4', 'G#4', 'G4', 'F#4', 'F4']): m.kazoo(at(z0, .3 + i * .5), [n], .45, .1)
[m.vo(w, 'cry', at(z0, 1.0 + i * .3), .35, .4, 'whimper', 1.2) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
print(round(END, 2)); m.write(sys.argv[1])
