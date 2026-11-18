"""Ep20 WRONG NUMBER sound: 8-bit chiptune brawl (new style for the series) + cartoon fight foley. vox2/fx2 only.
bump 0 · glare 2.6 · round1 4.2 · call1 7.6 · round2 10.0 · call2 14.2 · twist 17.2 · round3 20.4 · end 24.0 · END 26.6"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 26.6; m = Mix2(END, ep=20)
def chip(t0, t1, g=.6, bpm=150, root=('E3', 'G3', 'A3', 'B3')):
    b = 60 / bpm; t = t0; i = 0; arp = [0, 7, 12, 7, 3, 10, 15, 10]
    while t < t1 - .02:
        f = hz(root[(i // 8) % len(root)]) * 2 ** (arp[i % 8] / 12); d = b / 2 * .9; m.m(osc(f, d, 'sq') * env(int(d * SR), .002, .03) * .5, t, .07 * g, .2)
        if i % 4 == 0: m.m(osc(glide(160, 50, .12), .12, 'sq') * dec(.12, 25), t, .25 * g)
        if i % 4 == 2: m.m(hp(noise(.08), 2000) * dec(.08, 40), t, .12 * g)
        if i % 2 == 0: m.m(osc(f / 4, d * 2, 'tri') * env(int(d * 2 * SR), .005, .05), t, .14 * g, -.2)
        t += b / 2; i += 1
def ring(t, g=.25):
    for k in range(3): d = .25; m.f((osc(1300, d, 'sq') + osc(1600, d, 'sq')) * .5 * env(int(d * SR), .005, .03), t + k * .35, g)
def bus_horn(t): m.honk(t, .35); m.honk(t + .25, .3)
# BUMP
for i in range(8): m.footstep(.1 + i * .16, .25, -.4 + (i % 2) * .8)
m.vo('ronaldo', 'hmm', .3, .35, -.4); m.vo('messi', 'hmm', .5, .35, .4); m.thump(1.3, .9); m.smack(1.31, .8); m.vo('ronaldo', 'oof', 1.33, .6, -.2); m.vo('messi', 'ow', 1.36, .6, .2); m.f(hp(noise(.4), 800) * dec(.4, 6), 1.4, .25)
# GLARE: electric buzz + rising tension
t = 2.6; m.f(bp(noise(1.6), 2000, 6000) * (0.5 + 0.5 * np.sin(2 * np.pi * 30 * T(1.6))), t, .12); m.vo('ronaldo', 'grunt', t + .2, .5, -.3); m.vo('messi', 'hmph', t + .5, .5, .3); m.timpani(t + .3, 70, .35, roll=1.0)
# ROUND 1: windmill whiffs, flick, bin clang
t = 4.2; chip(t, t + 3.4, .8)
for i in range(8): m.whoosh(t + .2 + i * .22, .18, .15, i % 2 == 0, .3)
m.vo('messi', 'grunt', t + .5, .45, .3); m.vo('ronaldo', 'laugh', t + 1.0, .5, -.3, 'snicker'); m.squeak(t + 2.0, .4); m.whip(t + 2.02, .4); m.vo('messi', 'yelp', t + 2.05, .6, .3); m.slide_whistle(t + 2.1, True, .5, .25); m.clang(t + 2.6, .5, .5); m.thump(t + 2.62, .5); m.vo('ronaldo', 'siu', t + 2.6, .6, -.3)
# CALL 1
t = 7.6; m.vo('messi', 'cry', t + .1, .6, .3, 'sob', 1.2); ring(t + .3); bus_horn(t + 1.3); m.f(lp(noise(.8), 300) * env(int(.8 * SR), .1, .3), t + 1.2, .4)
# ROUND 2 v2: four clear hits (slap / headbutt / boot / punch) + lamp-post clonk
t = 10.0; chip(t, t + 4.2, .9, 170, ('A3', 'C4', 'D4', 'E4'))
m.whoosh(t + .4, .2, .3); m.smack(t + .55, 1.0, -.2); m.vo('ronaldo', 'yelp', t + .58, .6)
for i in range(5): m.footstep(t + 1.0 + i * .07, .3, .4)
m.thump(t + 1.35, .9); m.clang(t + 1.37, .25); m.vo('ronaldo', 'oof', t + 1.38, .6)
m.whip(t + 2.05, .35); m.thwack(t + 2.15, .9); m.vo('ronaldo', 'ow', t + 2.18, .6); m.slide_whistle(t + 2.2, True, .6, .3)
m.smack(t + 2.95, 1.0); m.boom(t + 2.96, .35); m.vo('ronaldo', 'yelp', t + 2.98, .6); m.clang(t + 3.3, .55, -.6); m.slide_whistle(t + 3.35, False, .4, .2)
m.vo('ronaldo', 'cry', t + 3.6, .6, -.4, 'wail', .6); m.crowd(t + 3.5, 'laugh', 0.8, .3); m.vo('messi', 'laugh', t + 3.65, .5, .4, 'point')
# CALL 2
t = 14.2; m.vo('ronaldo', 'hmph', t + .1, .5); ring(t + .3); bus_horn(t + 1.0); m.f(lp(noise(.8), 300) * env(int(.8 * SR), .1, .3), t + 1.0, .4); m.vo('ronaldo', 'laugh', t + 1.9, .5, 0, 'cackle')
# TWIST: record scratch, footsteps over, "?"
t = 17.2; m.scratch(t + .9, .5)
for i in range(8): m.footstep(t + 1.0 + i * .12, .25, .3)
m.vo('ronaldo', 'uhoh', t + 2.05, .6); m.wahwah(t + 2.2, .2); m.vo('bruno', 'laugh', t + 2.3, .5, .3, 'snicker')
# ROUND 3: everyone jumps, SPLAT, Messi crowns him
t = 20.4; chip(t, t + 3.6, 1.0, 180, ('E3', 'F3', 'G3', 'G#3'))
for i in range(8): m.vo(['generic_m', 'big', 'bruno', 'kid', 'generic_m', 'big', 'generic_m', 'kid'][i], 'yay', t + .05 + i * .06, .3, -.6 + i * .17)
m.slide_whistle(t + .2, False, .8, .3); m.boom(t + 1.0, .7); m.thump(t + 1.0, 1.0); m.vo('ronaldo', 'oof', t + 1.02, .7)
for k in range(6): m.smack(t + 1.1 + k * .08, .5)
m.crowd(t + 1.7, 'laugh', 1.8, .4); m.cork(t + 2.2, .3); m.vo('ronaldo', 'cry', t + 2.0, .55, 0, 'blubber', 1.4)
# END: high five + sob + chip sting
t = 24.0; m.smack(t + .3, .5); m.vo('messi', 'laugh', t + .4, .5, .3, 'giggle', .8); m.vo('bruno', 'laugh', t + .5, .5, -.3, 'belly', .8); m.vo('ronaldo', 'cry', t + .9, .5, 0, 'sob', 1.4)
for i, n in enumerate(['G4', 'F#4', 'F4', 'E4']): m.m(osc(hz(n), .3, 'sq') * env(int(.3 * SR), .005, .05) * .5, t + 1.2 + i * .3, .08)
m.write(sys.argv[1])
