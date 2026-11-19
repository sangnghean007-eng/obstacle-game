"""Ep23 DREAM DUO sound: phone-video feel. Each clip its own room tone + amateur crowd; one driving trap-style beat glues the montage (new for the series).
dirt 0 · cage 3.0 · futsal 5.6 · beach 8.4 · roof 11.2 · rain 14.2 · argue 17.6 · END 21.6"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 21.6; m = Mix2(END, ep=23)
def trap(t0, t1, g=.6, bpm=140):
    b = 60 / bpm; t = t0; i = 0
    while t < t1 - .02:
        if i % 8 in (0, 3, 6): m.m(osc(glide(90, 38, .45, .3), .45) * dec(.45, 4), t, .45 * g)
        if i % 8 == 4: m.snare(t, .22 * g)
        m.hat(t, .04 * g); m.hat(t + b / 4, .025 * g) if i % 2 else None; t += b / 2; i += 1
trap(0, 17.6, .7)
def room(t, d, lo, hi, g): m.f(bp(noise(d), lo, hi) * env(int(d * SR), .05, .1), t, g)
def amateur(t, g=.35): m.crowd(t, 'cheer', 1.2, g); m.vo('generic_m', 'yay', t + .05, .3, .5)
# DIRT: wind on the phone mic, nutmeg taps, bicycle, chickens
room(0, 3.0, 80, 600, .2); [m.thwack(.3 + i * .35, .25) for i in range(3)]; [m.vo('kid', 'yelp', .35 + i * .35, .35, .3) for i in range(3)]
m.whoosh(1.5, .4, .3); m.thwack(1.75, .8); m.vo('ronaldo', 'siu', 1.8, .5); m.thump(2.3, .4); m.honk(2.32, .25); m.f(osc(glide(900, 1300, .12), .12, 'saw') * dec(.12, 20) * .3, 2.4, .3); m.f(osc(glide(800, 1200, .12), .12, 'saw') * dec(.12, 20) * .3, 2.55, .3); amateur(2.35)
# CAGE: six taps, keeper spin, thud
t = 3.0; room(t, 2.6, 300, 2000, .1)
for i in range(6): m.thwack(t + .2 + i * .183, .3, (-1) ** i * .4)
m.spring(t + .6, .2, .8); m.vo('generic_m', 'uhoh', t + .9, .4); m.thwack(t + 1.3, .6); m.thump(t + 1.6, .6); m.vo('generic_m', 'oof', t + 1.62, .5); amateur(t + 1.55)
# FUTSAL: sneaker squeaks, domino clacks, chest thump, SIUUU echo
t = 5.6; room(t, 2.8, 500, 3000, .08)
for i in range(6): m.squeak(t + .1 + i * .18, .25)
for i in range(4): m.f(osc(1400 - i * 120, .06, 'sq') * dec(.06, 50) * .4, t + .35 + i * .22, .4)
m.thump(t + 1.6, .6); m.thwack(t + 1.85, .5); m.vo('ronaldo', 'siu', t + 1.95, .6); m.vo('ronaldo', 'siu', t + 2.25, .3); m.vo('ronaldo', 'siu', t + 2.5, .15); amateur(t + 1.95, .3)
# BEACH: waves, 8 header pings, POP
t = 8.4; room(t, 2.8, 100, 900, .2)
for i in range(8): m.f(osc(500 + i * 40, .08) * dec(.08, 30), t + .1 + i * .2, .35)
m.whoosh(t + 1.75, .3, .3); m.pop(t + 2.1, .8, 400); m.boom(t + 2.1, .3); amateur(t + 2.15)
# ROOF: night city, swirl, bonk, cool
t = 11.2; room(t, 3.0, 200, 1200, .08); m.thwack(t + .6, .6); m.f(osc(glide(600, 1400, 1.1) * (1 + .05 * np.sin(2 * np.pi * 10 * T(1.1))), 1.1, 'tri') * env(int(1.1 * SR), .05, .1), t + .6, .12); m.vo('ronaldo', 'yelp', t + .9, .4)
m.bonk(t + 1.7, .6); m.vo('ronaldo', 'oof', t + 1.72, .5); m.thump(t + 2.0, .4); m.cowbell(t + 2.2, .2); m.vo('messi', 'laugh', t + 2.3, .4, .3, 'snicker')
# RAIN: thunder, cross, header, rip, roar
t = 14.2; m.rain(t, 3.4, .12); m.boom(t + .1, .3); m.thwack(t + .85, .6); m.whoosh(t + 1.0, .5, .3); m.thwack(t + 1.4, .7); m.f(hp(noise(.4), 1500) * dec(.4, 8), t + 1.6, .5); m.crowd(t + 1.65, 'cheer', 2.0, .55); m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t + 2.2, 1.0, .25)
# ARGUE: two voices, run, crash, laugh
t = 17.6; m.rain(t, 4.0, .07); m.vo('ronaldo', 'hmph', t + .2, .5, -.3); m.vo('messi', 'hmph', t + .4, .5, .3); m.vo('ronaldo', 'siu', t + 1.0, .55, -.3); m.vo('messi', 'yay', t + 1.05, .5, .3)
m.thump(t + 1.5, .9); m.smack(t + 1.5, .8); m.vo('ronaldo', 'oof', t + 1.52, .6, -.2); m.vo('messi', 'ow', t + 1.55, .6, .2); m.crowd(t + 1.8, 'laugh', 1.8, .4); m.kazoo(t + 2.4, ['G4', 'E4', 'C4'], .25, .12)
m.write(sys.argv[1])
