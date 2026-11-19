"""Ep24 #1 v2 (multi-angle) sound. fc 0 · track 1.0 · ronrun 2.3 · wide 2.9 · gcam 3.3 (net 3.75) · keeper 4.2 · crowd 4.7 · cele 5.4 · END 6.4
Every cut gets its own sound perspective: close foley on the tracking cam, heavy breathing on Ronaldo's run, a whoosh-in on the behind-goal cam, crowd roar on the crowd cam."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 6.4; m = Mix2(END, ep=242)
m.f(bp(noise(END), 250, 2200) * .3, 0, .22)
m.brass_hit([hz('C4'), hz('G4')], .05, .4, .18); m.whoosh(.05, .3, .25, True, -.4); m.whoosh(.4, .3, .25, True, .4); m.thump(.62, .5)
for c in (1.0, 2.3, 2.9, 3.3, 4.2, 4.7, 5.4): m.whoosh(c - .04, .12, .12)  # cut swishes
for i in range(6): m.f(lp(noise(.05), 900) * dec(.05, 40), 1.0 + i * .22, .55, .3)
m.f(lp(noise(.5), 600) * env(int(.5 * SR), .02, .2), 1.5, .4, .4); m.vo('generic_m', 'oof', 1.6, .45, .4); m.vo('generic_m', 'yelp', 2.2, .45, .4)
for i in range(4): m.footstep(2.3 + i * .14, .4, -.4)
m.vo('ronaldo', 'grunt', 2.4, .45); m.f(hp(noise(.3), 1500) * env(int(.3 * SR), .1, .1), 2.6, .2)
m.f(lp(noise(.06), 700) * dec(.06, 30), 2.9, .5, .2); m.whoosh(2.95, .3, .2, True, -.2)
m.thwack(3.3, .9); m.f(osc(glide(200, 900, .45), .45, 'tri') * env(int(.45 * SR), .02, .05), 3.3, .2); m.boom(3.75, .5); m.f(hp(noise(.4), 800) * dec(.4, 8), 3.75, .6)
m.crowd(3.78, 'cheer', 2.6, .7); m.vo('generic_m', 'no', 4.25, .45, .3); m.thump(4.3, .4)
m.crowd(4.7, 'cheer', .9, .5); [m.vo(['generic_m', 'kid', 'big'][i], 'yay', 4.75 + i * .1, .35, -.5 + i * .5) for i in range(3)]
m.vo('ronaldo', 'siu', 5.45, .7); m.vo('messi', 'yay', 5.7, .5, .3); m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], 5.5, .8, .22)
m.write(sys.argv[1])
