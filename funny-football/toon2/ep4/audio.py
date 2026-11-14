"""Ep4 v3 "IMMOVABLE" sound: no TTS. Tuba march, crowd, synthesized grunts/hum/yawn and strong foley. All synthesized."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(hook=0, mission=1.8, push=3.8, tickle=6.2, decoy=8.6, dozer=11.0, team=13.6, flick=16.2, carry=18.2, thanks=20.6)
END = 23.2
m = Mix(END)
def tuba(f, t, d, g=.3): x = osc(f, d, 'saw') + .6 * osc(f, d, 'sq'); m.m(lp(x, 520) * env(len(x), .02, .08), t, g, 0, .12)
def march(t0, t1, g=1.0, bpm=112):
    b = 60 / bpm; line = ['D2', 'A1', 'D2', 'A1', 'F2', 'C2', 'F2', 'A1']; t = t0; i = 0
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


def sq(f, t, d, g=.12, pan=0): x = osc(f, d, 'sq'); m.f(lp(x, 3000) * env(len(x), .005, .04), t, g, pan, .1)
def level_start(t): [sq(hz(n), t + i * .09, .12, .12) for i, n in enumerate(['C5', 'E5', 'G5', 'C6'])]
def heart_lost(t): [sq(hz(n), t + i * .09, .14, .14) for i, n in enumerate(['E5', 'C5', 'G4'])]; m.pop(t, .25, 400)
def game_over(t): [sq(hz(n), t + i * .2, .26, .16) for i, n in enumerate(['G4', 'F4', 'E4', 'D4', 'C4'])]
def giggle(t, n=6): [voice(t + i * .13, .1, 420 - i * 8, 380 - i * 8, .3, -.3, 700, 2200) for i in range(n)]
def pins(t): [m.f(bp(noise(.08), 1500, 5000) * dec(.08, 40) + osc(900 + 300 * (i % 3), .08) * dec(.08, 50) * .4, t + i * .045, .35, np.random.uniform(-.7, .7), .3) for i in range(12)]

m.crowd(0, S['thanks'], .2, swell=False)
# HOOK
m.thud(0, 1.0); m.boing(0, .7, .55, 110, 300); m.crash(0, .35); voice(.02, .25, 380, 520, .45, -.3)
m.whoosh(.35, .35, .3, False, -.4); m.thud(.72, .6, -.4); m.tweet(.8, 3, .14, -.4); m.f(m.wav('ooh_crowd'), .45, .35, 0, .3)
march(.25, S['mission'], .7)
# MISSION
t = S['mission']; level_start(t + .15)
for k in range(6): m.footstep(t + k * .1, .25, -.5 + k * .1)
m.slurp(t + .3, 1.2, .3, .25); m.ding(t + .8, 1760, .2)
# 1 PUSH
t = S['push']; march(t, S['tickle'], .8, 112)
for k in range(3): voice(t + .1 + k * .55, .5, 150, 210, .42, -.3)
for k in range(12): m.footstep(t + k * .14, .22, -.4)
m.slurp(t + .4, 1.3, .3, .25); m.thud(t + 1.95, .5, -.4); heart_lost(t + 1.9)
# 2 TICKLE
t = S['tickle']; march(t, S['decoy'], .8, 120)
for k in range(10): m.tick(t + .3 + k * .12, k % 2 == 0, .1)
m.f(bp(noise(1.0), 3000, 8000) * (.5 + .5 * np.sin(2 * np.pi * 18 * T(1.0))) * .3, t + .3, .25, .3, .1)   # feather swish
giggle(t + 1.5, 7); heart_lost(t + 1.9)
# 3 DECOY
t = S['decoy']; march(t, S['dozer'], .8, 126)
m.ding(t + .3, 2093, .2); hm(t + .55, .5); m.pop(t + 1.0, .35, 900); m.whoosh(t + 1.0, .25, .2, False); m.slurp(t + 1.25, .6, .3, .25)
voice(t + 1.65, .4, 200, 160, .3, -.3, 400, 1200); heart_lost(t + 1.9)
# 4 BULLDOZER
t = S['dozer']; hit = t + 1.0
engine(t, 1.0, .45); m.whoosh(t + .5, .5, .3, True, -.3)
metal(hit, .6); m.thud(hit, 1.0); m.kick(hit, 1.0); m.crash(hit, .4)
for k in range(6): m.pop(hit + .1 + k * .12, .3, 500 + 300 * k)
yawn(hit + .25, .45); heart_lost(hit + .4)
march(hit + .6, S['team'], .7, 132)
# 5 TEAM ATTACK
t = S['team']; hit = t + 1.0
for k in range(16): m.footstep(t + k * .06, .3, -.6 + k * .05)
voice(t + .2, .6, 260, 340, .4, -.3, 600, 1800); voice(t + .3, .5, 200, 280, .35, -.1, 500, 1500)
m.f(lp(osc(glide(80, 400, .3, 2), .3, 'saw'), 1500) * env(int(.3 * SR), .05, .05), hit - .2, .3, 0, .3)
m.thud(hit, 1.0); m.kick(hit, 1.0); pins(hit + .02); m.crash(hit, .4); m.cheer_burst(hit + .1, .35)
# FLICK -> GAME OVER
t = S['flick']; tf = t + .75
m.f(osc(glide(90, 60, .6), .6) * env(int(.6 * SR), .2, .2), t + .1, .25, 0, .1)
m.pop(tf, .6, 1500); m.thwack(tf, .5); rise(tf + .02, .8, .3); m.whoosh(tf, .6, .45, True, -.5)
m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F4')], tf + .05, .8, .3); m.crash(tf, .4)
m.ding(t + 1.25, 3136, .35); heart_lost(tf + .2); game_over(t + 1.15)
m.f(m.wav('laugh_crowd'), tf + .2, .4, 0, .3)
# CARRY (twist)
t = S['carry']; m.f(osc(glide(2000, 500, .5, .8), .5) * env(int(.5 * SR), .01, .1), t, .25, -.2, .2); m.thud(t + .5, .5); m.boing(t + .5, .3, .35, 200, 400)
march(t + .6, S['thanks'], .9, 112); whistle_tune(t + .8, .2); m.cheer_burst(t + .6, .3)
# THANKS + FOLLOW
t = S['thanks']
for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'G5', 'E5', 'C6']): m.pluck(hz(n), t + .1 + i * .18, .6, .2, -.3 + i * .1, .5, .4)
m.saw_chord([hz('C4'), hz('E4'), hz('G4')], t + .1, 2.4, .05, 1600, 0, .3, .8, .4)
m.ding(t + 1.2, 2093, .35); m.pop(t + 1.2, .3); m.sparkle(t + 1.25, .5, .12)
m.f(m.wav('cheer_crowd'), t + .2, .25, 0, .3)
m.write(sys.argv[1])
