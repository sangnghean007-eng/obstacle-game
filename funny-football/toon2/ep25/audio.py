"""Ep25 NEW GEN vs OG sound: synthwave trailer (saw arps, gated drums, bass) for the new gen; record scratch + silence at the bump; heavenly choir + epic brass for the OGs; sad trombone + tiptoe pizzicato for the escape. vox2/fx2 only, original music."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('ti', 1.6), ('ya', 1.5), ('mb', 1.4), ('ha', 1.7), ('wk', 3.0), ('bp', 1.2), ('rv', 2.4), ('sh', 2.4), ('en', 2.4)]
ST = {}; _t = 0
for n, d in SEGS: ST[n] = _t; _t += d
END = _t; m = Mix2(END, ep=25); at = lambda n, z: ST[n] + z
def synthwave(t0, t1, g=.7, bpm=100):
    b = 60 / bpm; t = t0; i = 0; arp = ['A3', 'C4', 'E4', 'A4', 'F3', 'A3', 'C4', 'F4', 'C4', 'E4', 'G4', 'C5', 'G3', 'B3', 'D4', 'G4']; bass = ['A1', 'F1', 'C2', 'G1']
    while t < t1 - .02:
        n = arp[i % 16]; d = b / 4; m.m(lp(osc(hz(n), d * .9, 'saw'), 2600) * env(int(d * .9 * SR), .005, .05), t, .07 * g, .3 if i % 2 else -.3, .25)
        if i % 4 == 0: m.m(lp(osc(hz(bass[(i // 16) % 4]), b, 'saw'), 500) * env(int(b * SR), .01, .1), t, .22 * g)
        if i % 8 == 0: m.kick(t, .4 * g)
        if i % 8 == 4: m.snare(t, .3 * g); m.f(hp(noise(.3), 1500) * dec(.3, 6), t, .1 * g)
        t += d; i += 1
synthwave(at('ti', 0), at('bp', .5), .8)
m.boom(at('ti', 0), .5); m.f(osc(glide(40, 120, 1.4), 1.4, 'saw') * env(int(1.4 * SR), .5, .3) * .4, at('ti', .1), .25)
m.whoosh(at('ya', 0), .7, .35, True, -.4); m.f(bp(noise(.5), 2000, 5000) * env(int(.5 * SR), .02, .2), at('ya', .7), .35); m.vo('yamal', 'laugh', at('ya', .9), .45, 0, 'snicker')
m.whoosh(at('mb', 0), .6, .4, True, .4); m.f(lp(noise(.6), 1500) * env(int(.6 * SR), .05, .3), at('mb', .05), .3); m.vo('mbappe', 'hmph', at('mb', .8), .45)
m.vo('haaland', 'grunt', at('ha', .2), .6); m.thump(at('ha', 1.15), .9); m.clang(at('ha', 1.17), .3); m.vo('haaland', 'laugh', at('ha', 1.3), .5, 0, 'belly', .8)
for i in range(6): m.footstep(at('wk', i * .5), .5, (-1) ** i * .3)
m.f(osc(glide(200, 1200, 2.5), 2.5, 'saw') * env(int(2.5 * SR), 2.0, .2) * .25, at('wk', .5), .2)
m.thump(at('bp', .5), 1.0); m.smack(at('bp', .5), .7); m.scratch(at('bp', .52), .55); [m.vo(w, 'oof', at('bp', .55 + i * .05), .5, -.4 + i * .4) for i, w in enumerate(('yamal', 'mbappe', 'haaland'))]
m.choir([hz('C4'), hz('E4'), hz('G4'), hz('C5')], at('rv', .4), 2.0, .2); m.timpani(at('rv', .2), 70, .5, roll=1.0); m.brass_hit([hz('C3'), hz('G3'), hz('C4'), hz('E4')], at('rv', 1.3), 1.1, .3); m.sparkle(at('rv', .5), 1.5, .2); m.crowd(at('rv', 1.3), 'gasp', 1.0, .35)
m.vo('yamal', 'gasp', at('sh', .1), .5); m.thump(at('sh', .5), .6); m.vo('haaland', 'ow', at('sh', .52), .6); m.wahwah(at('sh', .8), .2)
t = at('sh', 1.4)
for i in range(8): m.pluck(hz(['C5', 'E5', 'C5', 'E5', 'D5', 'F5', 'D5', 'F5'][i]), t + i * .12, .1, .14, (-1) ** i * .3)
m.vo('ronaldo', 'laugh', at('en', .1), .55, -.3, 'belly', 1.0); m.vo('messi', 'laugh', at('en', .3), .5, .3, 'snicker'); m.brass_hit([hz('C4'), hz('E4'), hz('G4')], at('en', .1), .9, .2)
print(round(END, 2)); m.write(sys.argv[1])
