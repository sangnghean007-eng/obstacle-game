"""Ep24 #1 v4 sound, laid out per segment (segment start + z * slow factor)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('fc', 1.0, 1.3), ('track', 1.0, 1.3), ('slide', 1.0, 2.0), ('shout', 1.0, 2.0), ('track2', .6, 1.3), ('wide', .4, 1.5), ('gcam', .9, 1.8), ('fish', 1.0, 1.8), ('crowd', .9, 2.0), ('cele', 1.8, 1.7)]
ST = {}; _t = 0
for n, d, sl in SEGS: ST[n] = (_t, sl); _t += d * sl
END = _t; m = Mix2(END, ep=244)
at = lambda n, z: ST[n][0] + z * ST[n][1]
m.f(bp(noise(END), 250, 2200) * .3, 0, .22)
for n in ST: m.whoosh(at(n, 0) - .04, .12, .12)
m.brass_hit([hz('C4'), hz('G4')], at('fc', .05), .5, .18); m.whoosh(at('fc', .05), .3, .25, True, -.4); m.whoosh(at('fc', .4), .3, .25, True, .4); m.thump(at('fc', .62), .5)
for i in range(6): m.f(lp(noise(.05), 900) * dec(.05, 40), at('track', i * .17), .55, .3)
m.f(lp(noise(.7), 600) * env(int(.7 * SR), .02, .1), at('slide', 0), .5); m.vo('generic_m', 'yelp', at('slide', .25), .5); m.boom(at('slide', .35), .45); m.clang(at('slide', .36), .35); m.f(hp(noise(.5), 1500) * dec(.5, 6), at('slide', .36), .5)
m.f(hp(noise(.08), 3000) * dec(.08, 30), at('slide', .75), .5); m.crowd(at('slide', .5), 'laugh', 1.4, .4); m.vo('generic_m', 'hmm', at('slide', .85), .4)
m.vo('ronaldo', 'yelp', at('shout', .1), .7); m.vo('ronaldo', 'grunt', at('shout', .35), .6); m.thump(at('shout', .55), .6); m.f(hp(noise(.6), 2000) * env(int(.6 * SR), .1, .2), at('shout', .5), .3); m.vo('ronaldo', 'yelp', at('shout', .7), .6); m.squeak(at('shout', .8), .3)
for i in range(3): m.f(lp(noise(.05), 900) * dec(.05, 40), at('track2', i * .2), .5, .3)
m.f(lp(noise(.06), 700) * dec(.06, 30), at('wide', 0), .5, .2); m.whoosh(at('wide', .05), .4, .2, True, -.2)
m.thwack(at('gcam', 0), .9); m.f(osc(glide(150, 700, .8), .8, 'tri') * env(int(.8 * SR), .02, .05), at('gcam', 0), .2); m.boom(at('gcam', .45), .55); m.f(hp(noise(.4), 800) * dec(.4, 8), at('gcam', .45), .6); m.crowd(at('gcam', .47), 'cheer', 3.0, .7)
for i in range(8): m.f(lp(noise(.06), 1200) * dec(.06, 30), at('fish', i * .12), .35)
m.vo('generic_m', 'grunt', at('fish', .3), .45); m.vo('generic_m', 'grunt', at('fish', .55), .45, .4); m.f(osc(glide(400, 250, .4), .4, 'saw') * dec(.4, 6) * .3, at('fish', .6), .3); m.crowd(at('fish', .7), 'laugh', 1.0, .3)
m.crowd(at('crowd', 0), 'cheer', 1.6, .45); m.f(hp(noise(.08), 2000) * dec(.08, 30), at('crowd', .12), .4); m.f(hp(noise(.08), 2000) * dec(.08, 30), at('crowd', .57), .4); m.crowd(at('crowd', .6), 'laugh', 1.0, .3)
for i in range(6): m.footstep(at('cele', .05 + i * .1), .35)
m.whoosh(at('cele', .6), .3, .3, True); m.vo('ronaldo', 'siu', at('cele', .65), .8); m.thump(at('cele', 1.0), .45); m.vo('messi', 'hmph', at('cele', .5), .6, -.3)
for i in range(6): m.f(lp(noise(.04), 600) * dec(.04, 40), at('cele', .5 + i * .16), .2)
m.f(hp(noise(.05), 1200) * dec(.05, 40), at('cele', 1.47), .45); m.f(hp(noise(.05), 1200) * dec(.05, 40), at('cele', 1.6), .45); m.vo('messi', 'hmph', at('cele', 1.65), .5); m.crowd(at('cele', 1.5), 'laugh', 1.2, .3)
print(round(END, 2), round(at('track2', 0), 2), round(at('gcam', .9), 2))
m.write(sys.argv[1])
