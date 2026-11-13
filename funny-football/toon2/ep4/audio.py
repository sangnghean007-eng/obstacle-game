"""Episode 4 "THE HUMAN WALL" sound: strongman march, stadium, foley, 4 short Pico lines. All synthesized."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(hook=0, match=2.2, shield=5.0, yeet=10.0, brawl=12.6, press=15.8, bill=19.0, end=22.0, cta=24.4)
m = Mix(25.9)
def V5(name, t, g=1.0): m.put(m.vox, m.wav('lines5/' + name), t, g, 0, 0)
def whistle(t, d=.35, g=.3):
    tt = T(d); x = osc(2900 + 120 * np.sign(np.sin(2 * np.pi * 28 * tt)), d) + .3 * bp(noise(d), 2500, 4000); m.f(x * env(len(x), .01, .05), t, g, .2, .15)
def tuba(f, t, d, g=.3):
    x = osc(f, d, 'saw') + .6 * osc(f, d, 'sq'); m.m(lp(x, 500) * env(len(x), .02, .08), t, g, 0, .15)
def march(t0, t1, g=1.0):  # heavy, comedic strongman march (110 BPM, D minor)
    b = 60 / 110; line = ['D2', 'A1', 'D2', 'A1', 'F2', 'C2', 'F2', 'A1']; t = t0; i = 0
    while t < t1 - .05:
        tuba(hz(line[i % 8]), t, b * .8, .32 * g)
        m.kick(t, .7 * g) if i % 2 == 0 else m.snare(t, .35 * g)
        if i % 4 == 3: [m.snare(t + k * b / 4, .15 * g) for k in range(4)]
        m.hat(t + b / 2, .08 * g)
        if i % 8 == 0: m.brass_hit([hz('D3'), hz('A3'), hz('D4')], t, .3, .1 * g)
        t += b; i += 1
def creak(t, d=1.2, g=.25):
    tt = T(d); x = osc(55 + 8 * np.sin(2 * np.pi * 1.3 * tt), d, 'saw') * (.5 + .5 * np.sin(2 * np.pi * 17 * tt)); m.f(lp(x, 400) * env(len(x), .1, .2), t, g, 0, .1)
def squeak(t, g=.18, pan=-.3): d = .07; m.f(osc(glide(3200, 4200, d), d) * env(int(d * SR), .005, .02), t, g, pan, .05)
def kaching(t, g=.4): m.f(bp(noise(.15), 1500, 5000) * dec(.15, 30), t, g * .7); m.ding(t + .08, 2637, g); m.ding(t + .12, 3136, g * .8)
def falling(t, d=1.1, g=.25): m.f(osc(glide(2400, 500, d, .8), d) * env(int(d * SR), .02, .1), t, g, -.4, .2)
def powerup(t, d=.6, g=.3): m.f(lp(osc(glide(80, 400, d, 2), d, 'saw'), 1500) * env(int(d * SR), .05, .05), t, g, 0, .3)
def camclick(t, g=.25): m.f(bp(noise(.04), 2000, 7000) * dec(.04, 90), t, g, .4, .05); m.f(bp(noise(.03), 1000, 3000) * dec(.03, 90), t + .05, g * .6, .4, .05)

# stadium bed (except press room)
m.crowd(0, S['press'], .22, swell=False); m.crowd(S['bill'], 25.9 - S['bill'], .14, swell=False)

# HOOK
march(0, S['match'], .7)
for k in range(8): m.footstep(k * .1, .3, -.6 + k * .08); squeak(k * .1 + .05, .08)
V5('n_remember', 0.12)
m.thud(.8, .9); m.boing(.8, .6, .6, 120, 340); m.crash(.8, .3); m.whoosh(.85, .6, .35, True, -.6)
m.f(m.wav('ooh_crowd'), 1.0, .4, 0, .3)
# MATCH: 0-2 -> 3-2, sub on
t = S['match']; whistle(t + .05, .25, .2)
m.ding(t + .35, 1318, .25); m.ding(t + .5, 1046, .25)
for k in (.9, 1.3, 1.75): m.cheer_burst(t + k, .35); m.kick(t + k, .8); m.pop(t + k, .3, 600)
m.brass_hit([hz('C3'), hz('G3'), hz('C4'), hz('E4')], t + 1.75, .8, .22)
# SHIELD
t = S['shield']; march(t, S['yeet'], .8)
creak(t + .2, 1.3, .3)
for k in range(8): squeak(t + .3 + k * .16, .14, -.4)
m.boing(t + 1.6, .4, .35, 300, 600); m.thud(t + 1.65, .3)
V5('t_hm', t + 2.1)
m.f(osc(glide(500, 250, .6), .6) * env(int(.6 * SR), .1, .3) * .5, t + 2.45, .25, .2, .2)   # yawn hum
powerup(t + 3.3, .5, .35); m.boing(t + 3.5, .3, .3, 90, 60); m.whoosh(t + 3.55, .6, .45, False, -.5); m.crash(t + 3.55, .3)
m.f(m.wav('ooh_crowd'), t + 3.7, .35, 0, .3)
# YEET
t = S['yeet']
m.whoosh(t + .55, .2, .4, True, -.3); m.thwack(t + .6, .5); m.boing(t + .62, .5, .4, 200, 900)
falling(t + .7, 1.0, .22); m.sparkle(t + 1.5, .3, .15)
m.brass_hit([hz('F3'), hz('A3'), hz('C4'), hz('F4')], t + 1.35, .7, .25); m.crash(t + 1.35, .35); m.cheer_burst(t + 1.4, .3)
# BRAWL
t = S['brawl']; whistle(t + .05, .2, .25)
R = np.random.default_rng(4)
for k in range(22): (m.thud if k % 2 else m.pop)(t + .1 + k * .07 + R.random() * .03, .35, 300 + R.random() * 900) if k % 2 == 0 else m.thud(t + .1 + k * .07, .35, R.uniform(-.6, .6))
for k in range(8): m.snare(t + k * .12, .3, R.uniform(-.5, .5))
m.scratch(t + .9, .35); m.boing(t + .6, .25, .3, 500, 200)
m.crowd(t, 1.6, .35)
for k in range(4): m.footstep(t + 1.2 + k * .1, .3, .5)
whistle(t + 1.6, .9, .38)
m.brass_hit([hz('C2'), hz('F#2'), hz('C3')], t + 1.85, .9, .3)
# PRESS
t = S['press']
for k in range(7): camclick(t + .1 + k * .38 + (k % 2) * .1, .22)
m.music_box(t + .2, ['E5', 'C5', 'A4', None, 'E5', 'D5', 'B4'], .3, .12)
V5('c_saved', t + .55)
# BILL
t = S['bill']
m.whoosh(t + .2, .9, .25, False)
kaching(t + 1.15, .4); kaching(t + 1.6, .35)
m.brass_hit([hz('D3'), hz('F3'), hz('A3')], t + 1.5, .5, .2)
# END
t = S['end']; march(t, S['cta'], .75)
V5('n_who', t + .2)
for k in range(4): m.boing(t + .55 + k * .55, .3, .35, 160, 420)
m.badumtss(t + 1.95, .4)
# CTA
t = S['cta']; m.ding(t + .05, 1568, .3); m.ding(t + .55, 2093, .3); m.pop(t + .5, .3)
V5('n_follow', t + .2)
m.write(sys.argv[1])
