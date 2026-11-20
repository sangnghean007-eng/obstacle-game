"""Ep29 THE WATCH PARTY sound: living-room party funk (new style: slap-bass + clavinet house-party groove) that cuts to a tinny TV-broadcast
mix for every match moment (band-passed crowd + commentator-style stings, no words); party poppers, kazoos, horns, doorbell, a sad record-scratch at the door."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('r0', 1.8), ('m1', 2.2), ('r1', 2.6), ('m2', 3.0), ('r2', 3.0), ('m3', 1.9), ('r3', 1.8), ('m4', 2.4), ('r4', 1.8), ('m5', 1.9), ('r5', 1.8), ('m6', 2.4), ('r6', 4.6)]
ST = {}; _t = 0
for n, d in SEGS: ST[n] = _t; _t += d
END = _t; m = Mix2(END, ep=29); at = lambda n, z: ST[n] + z
def funk(t0, t1, g=.5, bpm=112, hype=1.0):
    b = 60 / bpm; t = t0; i = 0; bass = ['E2', 'E2', 'G2', 'E2', 'A2', 'E2', 'D2', 'B1']
    while t < t1 - .03:
        if i % 2 == 0: m.m(lp(osc(hz(bass[(i // 2) % 8]), .18, 'saw'), 700) * dec(.18, 10), t, .45 * g)
        if i % 4 == 2: m.snare(t, .22 * g * hype)
        if i % 4 == 0: m.m(osc(glide(110, 45, .25), .25) * dec(.25, 9), t, .5 * g)
        if i % 2 == 1: m.m(bp(osc(hz(['E4', 'G4', 'B4', 'D5'][i % 4]), .09, 'sq'), 600, 3000) * dec(.09, 25), t, .12 * g * hype)
        m.hat(t, .035 * g); t += b / 2; i += 1
def tvbed(t0, t1, g=.25):  # tinny broadcast crowd
    n = int((t1 - t0) * SR); m.f(bp(noise(t1 - t0), 500, 2500) * env(n, .1, .2), t0, g)
def roomBeats():
    for n in ('r0', 'r1', 'r2', 'r3', 'r4', 'r5'): funk(at(n, 0), at(n, dict(SEGS)[n]), .55 if n in ('r0', 'r1', 'r4') else .8, hype=.5 if n in ('r1', 'r4') else 1.2)
roomBeats()
for n in ('m1', 'm2', 'm3', 'm4', 'm5', 'm6'): tvbed(at(n, 0), at(n, dict(SEGS)[n]), .2)
# room 0: popcorn crunch, remote click
for i in range(4): m.f(hp(noise(.04), 2000) * dec(.04, 50), at('r0', .3 + i * .25), .2)
m.f(osc(1500, .03) * dec(.03, 60), at('r0', 1.6), .3)
# m1 14': goal, broadcast roar, SIUUU on TV
m.whoosh(at('m1', .4), .3, .35, True); m.thump(at('m1', .7), .6); m.crowd(at('m1', .75), 'cheer', 1.2, .35); m.vo('ronaldo', 'siu', at('m1', .9), .6)
# r1 fake congrats: limp slow claps, sigh, party blower deflates
for i in range(5): m.clap(at('r1', .4 + i * .35), .25)
m.vo('messi', 'hmm', at('r1', .7), .35); m.f(osc(glide(500, 300, .8), .8, 'saw') * env(int(.8 * SR), .05, .3), at('r1', 1.3), .08); m.vo('generic_m', 'hmph', at('r1', 1.8), .35)
# m2 penalty: tension, BOING off the post, bonk, crowd gasp
m.timpani(at('m2', 0), 70, .3, roll=.8); m.whip(at('m2', .9), .5); m.spring(at('m2', 1.25), .5, .6); m.clang(at('m2', 1.25), .5); m.bonk(at('m2', 1.58), .7); m.vo('ronaldo', 'ow', at('m2', 1.6), .5); m.crowd(at('m2', 1.7), 'gasp', 1.0, .3); m.xylo_fall(at('m2', 2.0), .15)
# r2 the real party: poppers, SIUUU mock, laughs, horns
for k in (.05, .15): m.cork(at('r2', k), .6)
m.boom(at('r2', .1), .4); m.vo('generic_m', 'siu', at('r2', .3), .6); [m.vo(w, 'laugh', at('r2', .6 + i * .15), .45, -.4 + i * .4, 'belly') for i, w in enumerate(('generic_m', 'messi', 'big'))]; m.honk(at('r2', 1.0), .3); m.honk(at('r2', 1.3), .3)
# m3 45+1' Galeno
m.thump(at('m3', .7), .6); m.crowd(at('m3', .75), 'cheer', 1.0, .35); m.vo('generic_m', 'yay', at('m3', 1.0), .4)
# r3 party horns
for i in range(4): m.honk(at('r3', .1 + i * .3), .35)
m.vo('messi', 'laugh', at('r3', .4), .4, 0, 'giggle')
# m4 VAR + Toney no-look penalty
m.f(osc(880, .15, 'sq') * env(int(.15 * SR), .01, .05), at('m4', .1), .15); m.f(osc(660, .15, 'sq') * env(int(.15 * SR), .01, .05), at('m4', .3), .15); m.whip(at('m4', .5), .5); m.thump(at('m4', .7), .6); m.crowd(at('m4', .75), 'cheer', 1.2, .35)
# r4 the deadpan no-look stare: record scratch + silence-ish groove
m.f(bp(noise(.25), 800, 3000) * env(int(.25 * SR), .01, .1), at('r4', 0), .4); m.f(osc(glide(300, 900, .2), .2) * dec(.2, 8), at('r4', .02), .2); m.xylo(at('r4', .8), ['C5', 'C5'], .25, .12)
# m5 75' Ibañez header
m.f(lp(osc(2900, .3, 'sq'), 5000) * env(int(.3 * SR), .01, .05), at('m5', .0), .06); m.bonk(at('m5', .35), .4); m.thump(at('m5', .7), .6); m.crowd(at('m5', .75), 'cheer', 1.0, .35)
# r5 conga: kazoo melody
m.kazoo(at('r5', .05), ['C5', 'D5', 'E5', 'C5', 'G5', 'E5', 'C5'], .24, .14)
# m6 FT + table slide
m.f(lp(osc(2900, 1.0, 'sq'), 5000) * env(int(1.0 * SR), .01, .1), at('m6', .0), .06); m.slide_whistle(at('m6', .4), False, .8, .3); m.wahwah(at('m6', 1.2), .2)
# r6 doorbell, panic cleanup, fake sympathy, banner flip
m.f(osc(988, .35) * dec(.35, 5), at('r6', .0), .4); m.f(osc(784, .5) * dec(.5, 4), at('r6', .25), .35)
m.f(bp(noise(.3), 800, 3000) * env(int(.3 * SR), .01, .1), at('r6', .05), .4); m.whoosh(at('r6', .5), .4, .4); m.f(lp(noise(.6), 400) * dec(.6, 5), at('r6', 1.0), .3)
for i in range(3): m.footstep(at('r6', 1.4 + i * .2), .3)
m.vo('messi', 'hmm', at('r6', 1.9), .35); m.vo('ronaldo', 'hmph', at('r6', 2.6), .45); m.whoosh(at('r6', 2.9), .3, .35); m.vo('generic_m', 'laugh', at('r6', 3.05), .4, -.3, 'snicker')
n = int(1.6 * SR); m.m(lp(osc(hz('E2'), 1.6, 'saw'), 500) * env(n, .1, .6) * .4, at('r6', .5), 1.0); funk(at('r6', 3.0), END - .05, .55, hype=.6)
print(round(END, 2)); m.write(sys.argv[1])
