"""Dream Duo #2 sound: cheeky pizzicato for Messi's dribble, a dreamy harp + 'awww' when Ronaldo is star-struck, record scratch for the miss, a huge SLAP with hit-stop silence, then a pounding beat for the goal run and a stadium roar for the double SIUUU."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('fc2', 1.0, 1.2), ('dr1', 1.2, 1), ('aw1', 1.0, 1.1), ('dr2', 1.2, 1), ('aw2', 1.0, 1), ('miss', 2.0, 1), ('slap', 2.2, 1), ('goals', 4.5, 1), ('siu2', 2.4, 1), ('card2', 2.6, 1)]
ST = {}; _t = 0
for n, d, sl in SEGS: ST[n] = (_t, sl); _t += d * sl
END = _t; m = Mix2(END, ep=245); at = lambda n, z: ST[n][0] + z * ST[n][1]
m.f(bp(noise(END), 250, 2200) * .3, 0, .2)
for n in ST: m.whoosh(at(n, 0) - .04, .12, .1)
def pizz(t0, t1, g=.5):
    notes = ['E4', 'G4', 'B4', 'E5', 'D5', 'B4', 'G4', 'A4']; t = t0; i = 0
    while t < t1 - .02: m.pluck(hz(notes[i % 8]), t, .12, .12 * g, .2, 1.4); t += .14; i += 1
m.brass_hit([hz('C4'), hz('G4')], .05, .4, .18); m.whoosh(.1, .3, .25, True, -.4); m.whoosh(.45, .3, .25, True, .4)
pizz(at('dr1', 0), at('dr1', 1.2)); [m.f(lp(noise(.05), 900) * dec(.05, 40), at('dr1', i * .18), .5, .3) for i in range(7)]; m.vo('generic_m', 'oof', at('dr1', .4), .45); m.vo('generic_m', 'yelp', at('dr1', .85), .45)
m.harp_gliss(at('aw1', 0), ['C5', 'E5', 'G5', 'C6', 'E6', 'G6'], .06, .18); m.vo('ronaldo', 'hmm', at('aw1', .2), .5); m.crowd(at('aw1', .2), 'gasp', .9, .25); m.sparkle(at('aw1', .1), .9, .2)
pizz(at('dr2', 0), at('dr2', 1.2)); m.whoosh(at('dr2', .2), .3, .25); m.vo('generic_m', 'oof', at('dr2', .5), .45); m.vo('generic_m', 'yelp', at('dr2', .78), .45); m.clang(at('dr2', .95), .4); m.vo('big', 'oof', at('dr2', .97), .45, -.3); m.vo('generic_m', 'oof', at('dr2', 1.0), .45, .3); m.crowd(at('dr2', 1.0), 'laugh', .8, .3)
m.harp_gliss(at('aw2', 0), ['G5', 'B5', 'D6', 'G6'], .07, .16); [m.f(hp(noise(.04), 1500) * dec(.04, 60), at('aw2', i * .125), .35) for i in range(8)]; m.vo('ronaldo', 'yay', at('aw2', .3), .45)
m.thwack(at('miss', .3), .5); [m.f(hp(noise(.04), 1500) * dec(.04, 60), at('miss', .2 + i * .125), .3) for i in range(7)]; m.slide_whistle(at('miss', .7), False, .5, .2); m.scratch(at('miss', 1.2), .55); m.crowd(at('miss', 1.25), 'gasp', 1.0, .4); m.wahwah(at('miss', 1.3), .18)
[m.footstep(at('slap', i * .15), .45) for i in range(6)]; m.f(hp(noise(.8), 2000) * env(int(.8 * SR), .1, .2), at('slap', .1), .2); m.vo('messi', 'grunt', at('slap', .85), .6)
m.whip(at('slap', .9), .4); m.smack(at('slap', 1.0), 1.0); m.boom(at('slap', 1.0), .5); m.vo('ronaldo', 'yelp', at('slap', 1.12), .7); m.crowd(at('slap', 1.15), 'gasp', 1.0, .45); m.f(osc(1200, .3) * dec(.3, 10), at('slap', 1.5), .2); m.vo('ronaldo', 'grunt', at('slap', 1.6), .5)
g0 = at('goals', 0); b = 60 / 150; t = g0; i = 0
while t < at('goals', 4.5) - .02: (m.kick(t, .45) if i % 2 == 0 else m.snare(t, .25)); m.hat(t + b / 2, .06); t += b; i += 1
for j in range(3): k0 = at('goals', j * 1.5); m.thwack(k0 + .15, .5); m.thwack(k0 + .75, .8); m.boom(k0 + .93, .4); m.crowd(k0 + .95, 'cheer', 1.2, .55); m.vo(['ronaldo', 'messi', 'ronaldo'][j], 'yay', k0 + 1.0, .5)
for n in ('ronaldo', 'messi'): m.vo(n, 'siu', at('siu2', .8), .6, -.3 if n == 'ronaldo' else .3)
m.thump(at('siu2', 1.35), .7); m.crowd(at('siu2', 1.3), 'cheer', 2.6, .7); m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], at('siu2', 1.35), 1.2, .25); m.firework(at('siu2', 1.6), .3)
m.kazoo(at('card2', .1), ['C5', 'E5', 'G5', 'C6'], .14, .12)
print(round(END, 2)); m.write(sys.argv[1])
