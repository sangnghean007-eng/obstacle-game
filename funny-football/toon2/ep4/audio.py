"""Ep4 v3 "IMMOVABLE" sound: no TTS. Tuba march, crowd, synthesized grunts/hum/yawn and strong foley. All synthesized."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(impact=0, push=1.4, piggy=4.0, dozer=6.6, flick=9.4, walk=11.4, loop=13.4)
END = 14.4
m = Mix(END)
def tuba(f, t, d, g=.3): x = osc(f, d, 'saw') + .6 * osc(f, d, 'sq'); m.m(lp(x, 520) * env(len(x), .02, .08), t, g, 0, .12)
def march(t0, t1, g=1.0):
    b = 60 / 112; line = ['D2', 'A1', 'D2', 'A1', 'F2', 'C2', 'F2', 'A1']; t = t0; i = 0
    while t < t1 - .05:
        tuba(hz(line[i % 8]), t, b * .8, .34 * g)
        (m.kick(t, .7 * g) if i % 2 == 0 else m.snare(t, .3 * g)); m.hat(t + b / 2, .07 * g)
        if i % 4 == 2: m.pluck(hz(['A4', 'D5', 'F5', 'E5'][(i // 4) % 4]), t, .3, .12 * g, .3)
        t += b; i += 1
def voice(t, d, f0, f1, g=.4, pan=0, lo=500, hi=1600, buzz=1.0):  # grunts made from a buzzy source through a mouth-like band
    tt = T(d); f = glide(f0, f1, d) * (1 + .03 * np.sin(2 * np.pi * 7 * tt)); x = osc(f, d, 'saw') * buzz + .3 * osc(f * 2, d)
    y = bp(x, lo, hi) + .4 * bp(x, hi * 1.6, hi * 2.2); y *= env(len(y), .03, .1) * (1 + .3 * np.sin(2 * np.pi * 11 * tt)); m.put(m.vox, y, t, g, pan, .03)
def hm(t, g=.5): d = .38; tt = T(d); x = osc(glide(115, 165, d, 2), d) + .25 * osc(glide(230, 330, d, 2), d); m.put(m.vox, lp(x, 600) * env(len(x), .03, .12), t, g, .2, .02)
def yawn(t, g=.4): voice(t, 1.0, 260, 120, g, .2, 350, 1100, .7)
def engine(t, d, g=.3):
    tt = T(d); f = 45 + 25 * tt / d; x = osc(f, d, 'saw') * (.6 + .4 * np.sign(np.sin(2 * np.pi * 14 * tt))); m.f(lp(x, 500) * env(len(x), .1, .05) * (.4 + .6 * tt / d), t, g, -.4, .05)
def metal(t, g=.5):
    m.f(bp(noise(.6), 800, 6000) * dec(.6, 7), t, g, 0, .4)
    for f in (523, 811, 1307, 1999): d = 1.0; m.f(osc(f, d) * dec(d, 5), t + .01, g * .25, np.random.uniform(-.5, .5), .4)
def rise(t, d=.7, g=.3): m.f(osc(glide(400, 2600, d, .6), d) * env(int(d * SR), .01, .1), t, g, -.4, .2)
def whistle_tune(t, g=.18):
    for i, n in enumerate(['G6', 'B6', 'D7', 'B6', 'A6', 'G6', None, 'D7', 'C7']):
        if n: d = .2; tt = T(d); m.f(osc(hz(n) * (1 + .01 * np.sin(2 * np.pi * 6 * tt)), d) * env(int(d * SR), .02, .05), t + i * .2, g, .3, .3)

m.crowd(0, END, .2, swell=False)
# IMPACT at frame 0
m.thud(0, 1.0); m.boing(0, .7, .55, 110, 300); m.crash(0, .35); voice(.02, .25, 380, 520, .45, -.3)   # "oof"
march(.25, 7.55, .8)
m.whoosh(.35, .35, .3, False, -.4); m.thud(.72, .6, -.4); m.tweet(.8, 3, .14, -.4); m.f(m.wav('ooh_crowd'), .45, .35, 0, .3)
# 1 PUSH + sip
t = S['push']
for k in range(4): voice(t + .1 + k * .55, .5, 150, 210, .42, -.3)        # "hnnngh"
for k in range(16): m.footstep(t + k * .14, .22, -.4); m.f(osc(glide(3200, 4200, .06), .06) * env(int(.06 * SR), .005, .02), t + k * .14 + .05, .06, -.4, .05)
m.slurp(t + .7, 1.4, .35, .25)
# 2 PIGGYBACK + phone
t = S['piggy']
m.boing(t + .1, .45, .4, 200, 500); m.thud(t + .45, .35, .3)
for k in range(3): voice(t + .7 + k * .6, .4, 220, 300, .35, .3, 600, 1800)  # angry "grr"
for k in range(10): m.tick(t + .6 + k * .17, k % 2 == 0, .12)
hm(t + 1.3, .55)
# 3 BULLDOZER -> crash, yawn
t = S['dozer']; hit = t + 1.0
engine(t, 1.0, .45); m.whoosh(t + .5, .5, .3, True, -.3)
metal(hit, .6); m.thud(hit, 1.0); m.kick(hit, 1.0); m.crash(hit, .4)
for k in range(6): m.pop(hit + .1 + k * .12, .3, 500 + 300 * k)
m.boing(hit + .35, .3, .5, 300, 150)
yawn(hit + .25, .45)
march(hit + .9, S['flick'], .6)
# FLICK: the topper
t = S['flick']; tf = t + .75
m.f(osc(glide(90, 60, .6), .6) * env(int(.6 * SR), .2, .2), t + .1, .25, 0, .1)  # tense hold
m.pop(tf, .6, 1500); m.thwack(tf, .5); rise(tf + .02, .8, .3); m.whoosh(tf, .6, .45, True, -.5)
m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F4')], tf + .05, .8, .3); m.crash(tf, .4)
m.ding(t + 1.4, 3136, .35); m.sparkle(t + 1.35, .4, .14)
m.f(m.wav('laugh_crowd'), tf + .2, .4, 0, .3)
# WALK OFF with the flag
t = S['walk']; march(t, S['loop'], .9); whistle_tune(t + .2, .2); m.cheer_burst(t + .1, .3)
m.ding(t + 1.4, 1568, .25)
# LOOP: tiny revenge run
t = S['loop']
for k in range(8): m.footstep(t + k * .1, .3, -.6 + k * .1)
voice(t + .3, .6, 200, 330, .4, -.3, 600, 1800)
m.whoosh(t + .6, .4, .3, True, -.2)
m.write(sys.argv[1])
