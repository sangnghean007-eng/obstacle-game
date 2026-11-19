"""Ep24 Dream Duo (realistic) #1 sound: stadium bed + broadcast-style build; real football foley (close touches, slide tackle, side-foot, net), crowd swell into the goal.
face 0–1 · play 1–5.3 (shot 3.2, goal 3.5)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 5.3; m = Mix2(END, ep=241)
m.f(bp(noise(END), 250, 2200) * .3, 0, .25)
m.brass_hit([hz('C4'), hz('G4')], .05, .4, .18); m.whoosh(.05, .3, .25, True, -.4); m.whoosh(.4, .3, .25, True, .4); m.thump(.62, .5)
P = 1.0
for i in range(8): m.f(lp(noise(.05), 900) * dec(.05, 40), P + i * .22, .45, .3)
m.f(lp(noise(.5), 600) * env(int(.5 * SR), .02, .2), P + .5, .35, .4); m.vo('generic_m', 'oof', P + .6, .4, .4); m.crowd(P + .6, 'gasp', .8, .25, .3)
m.vo('generic_m', 'yelp', P + 1.2, .4, .4); m.crowd(P + 1.2, 'gasp', .8, .3, .2)
m.f(lp(noise(.06), 700) * dec(.06, 30), P + 1.85, .5, .2); m.whoosh(P + 1.9, .3, .2, True, -.2)
for i in range(6): m.footstep(P + .9 + i * .2, .3, -.4)
m.thwack(P + 2.2, .8, -.2); m.whoosh(P + 2.22, .3, .3); m.f(hp(noise(.4), 800) * dec(.4, 8), P + 2.5, .5); m.thump(P + 2.5, .4)
m.crowd(P + 2.5, 'cheer', 1.8, .65); m.vo('ronaldo', 'siu', P + 2.75, .6); m.vo('messi', 'yay', P + 2.9, .45, .3)
m.write(sys.argv[1])
