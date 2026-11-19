"""Ep24 #1 v3 (gags) sound. fc 0 · track 1.0 · slide 2.0 (crash 2.25) · shout 2.7 · track2 3.4 · wide 4.0 · gcam 4.4 (net 4.85) · fish 5.3 · crowd 6.0 · cele 6.7 (SIUUU 7.4, ASSIST? 7.15, pat 8.15) · END 8.5"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 8.5; m = Mix2(END, ep=243)
m.f(bp(noise(END), 250, 2200) * .3, 0, .22)
m.brass_hit([hz('C4'), hz('G4')], .05, .4, .18); m.whoosh(.05, .3, .25, True, -.4); m.whoosh(.4, .3, .25, True, .4); m.thump(.62, .5)
for c in (1.0, 2.0, 2.7, 3.4, 4.0, 4.4, 5.3, 6.0, 6.7): m.whoosh(c - .04, .12, .12)
for i in range(5): m.f(lp(noise(.05), 900) * dec(.05, 40), 1.0 + i * .2, .55, .3)
# slide into the ad boards
m.f(lp(noise(.4), 600) * env(int(.4 * SR), .02, .1), 2.0, .5); m.vo('generic_m', 'yelp', 2.15, .5); m.boom(2.25, .4); m.clang(2.27, .35); m.f(hp(noise(.5), 1500) * dec(.5, 6), 2.27, .5); m.crowd(2.4, 'laugh', 1.0, .35)
# Ronaldo shouting PASS
m.vo('ronaldo', 'yelp', 2.75, .7); m.vo('ronaldo', 'grunt', 3.0, .6); m.vo('ronaldo', 'yelp', 3.15, .6); m.f(osc(1000, .05) * dec(.05, 50), 3.0, .1)
for i in range(3): m.f(lp(noise(.05), 900) * dec(.05, 40), 3.45 + i * .2, .5, .3)
m.f(lp(noise(.06), 700) * dec(.06, 30), 4.0, .5, .2); m.whoosh(4.05, .3, .2, True, -.2)
m.thwack(4.4, .9); m.f(osc(glide(200, 900, .45), .45, 'tri') * env(int(.45 * SR), .02, .05), 4.4, .2); m.boom(4.85, .5); m.f(hp(noise(.4), 800) * dec(.4, 8), 4.85, .6); m.crowd(4.88, 'cheer', 2.8, .7)
# keeper flapping in the net like a fish
for i in range(6): m.f(lp(noise(.06), 1200) * dec(.06, 30), 5.35 + i * .11, .35); m.vo('generic_m', 'whistle' if False else 'grunt', 5.5, .4)
m.f(osc(glide(500, 300, .3), .3) * dec(.3, 6), 5.7, .25)
# crowd + sign flips
m.crowd(6.0, 'cheer', .9, .5); m.f(hp(noise(.08), 2000) * dec(.08, 30), 6.12, .4); m.f(hp(noise(.08), 2000) * dec(.08, 30), 6.57, .4)
# celebration gag
for i in range(5): m.footstep(6.75 + i * .12, .35)
m.whoosh(7.3, .3, .3, True); m.vo('ronaldo', 'siu', 7.35, .8); m.thump(7.7, .4); m.vo('messi', 'hmph', 7.15, .6, -.3); m.f(lp(noise(.04), 600) * dec(.04, 40), 7.2, .2); m.f(lp(noise(.04), 600) * dec(.04, 40), 7.37, .2)
m.f(hp(noise(.05), 1200) * dec(.05, 40), 8.15, .4); m.f(hp(noise(.05), 1200) * dec(.05, 40), 8.3, .4); m.crowd(8.1, 'laugh', .5, .3)
m.write(sys.argv[1])
