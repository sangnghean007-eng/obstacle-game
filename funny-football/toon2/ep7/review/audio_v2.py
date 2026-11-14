"""Ep7 GOAT COURT sound: courtroom drama score, gavel, per-exhibit stingers and foley, cartoon mumbles. No TTS."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(open=0, ballon=2.4, ucl=6.6, wc=10.8, intl=14.8, assist=19.0, verdict=22.8, thanks=26.7)
END = 29.5
m = Mix(END)
def voice(t, d, f0, f1, g=.4, pan=0, lo=500, hi=1600, buzz=1.0):
    tt = T(d); f = glide(f0, f1, d) * (1 + .03 * np.sin(2 * np.pi * 7 * tt)); x = osc(f, d, 'saw') * buzz + .3 * osc(f * 2, d)
    y = bp(x, lo, hi) + .4 * bp(x, hi * 1.6, hi * 2.2); y *= env(len(y), .03, .1) * (1 + .3 * np.sin(2 * np.pi * 11 * tt)); m.put(m.vox, y, t, g, pan, .03)
def mumble(t, n, f0, g=.3, pan=0):
    R = np.random.default_rng(int(t * 100))
    for i in range(n): f = f0 * (1 + R.uniform(-.25, .3)); d = .07 + R.random() * .04; x = bp(osc(f, d, 'saw'), 500, 2500) * env(int(d * SR), .005, .03); m.put(m.vox, x, t + i * .1, g, pan, .02)
def gavel(t, g=.9): m.f(bp(noise(.15), 300, 2500) * dec(.15, 40) + osc(glide(220, 120, .15), .15) * dec(.15, 30), t, g, 0, .5)
def strings(t, d, notes, g=.1): m.saw_chord([hz(n) for n in notes], t, d, g, 1200, 0, .25, .3, .5)
def drama(t0, t1, g=1.0):  # original courtroom suspense bed: low strings pulse + timpani
    b = 60 / 92; t = t0; i = 0; prog = [['D3', 'F3', 'A3'], ['A#2', 'D3', 'F3'], ['C3', 'E3', 'G3'], ['A2', 'C#3', 'E3']]
    while t < t1 - .05:
        strings(t, 4 * b * .95, prog[i % 4], .07 * g)
        for k in range(4): m.f(osc(glide(90, 60, .25), .25) * dec(.25, 12), t + k * b, .22 * g, 0, .2)   # timpani
        m.bass(hz(prog[i % 4][0]) / 2, t, 4 * b * .9, .25 * g)
        t += 4 * b; i += 1
def clink(t, g=.3, f=1500): d = .5; x = sum(a * osc(f * k, d) for k, a in [(1, 1), (2.7, .5), (5.2, .25)]) * dec(d, 9); m.f(x, t, g, np.random.uniform(-.4, .4), .3)
def bleat(t, g=.4): d = .6; tt = T(d); f = 520 * (1 + .12 * np.sign(np.sin(2 * np.pi * 14 * tt))); x = bp(osc(f, d, 'saw'), 600, 2600) * env(int(d * SR), .03, .15); m.put(m.vox, x, t, g, 0, .1)
def chew(t, d=1.4): [m.f(bp(noise(.06), 800, 4000) * dec(.06, 50), t + k * .11, .25, 0, .05) for k in range(int(d / .11))]
def burp(t): voice(t, .5, 110, 80, .5, 0, 150, 600, 1.0)
def choir(t, d=1.6): m.choir([hz('D4'), hz('F#4'), hz('A4'), hz('D5')], t, d, .2)
def stinger(t, notes, g=.25): m.brass_hit([hz(n) for n in notes], t, .6, g); m.crash(t, .2)

m.crowd(0, S['thanks'], .1, swell=False)
# OPEN
gavel(.25); gavel(.6); bleat(.85, .35); m.f(m.wav('ooh_crowd'), .9, .3, 0, .3)
for k in range(8): m.footstep(1.0 + k * .07, .25, -.6 + k * .17)
m.f(osc(glide(3000, 3400, .4), .4) * .2 * env(int(.4 * SR), .02, .1), 1.6, .15, 0, .1)   # sparks
drama(1.2, S['verdict'], .9)
# EXHIBIT 1: Ballon d'Or towers
t = S['ballon']; stinger(t, ['D3', 'A3', 'D4'])
for i in range(8): clink(t + i * .18, .22, 1300 + i * 120)
for i in range(5): clink(t + .3 + i * .25, .2, 1000 + i * 90)
voice(t + 2.0, .5, 160, 230, .35, .3)
m.f(osc(glide(300, 200, .6), .6) * .3 * (1 + np.sin(2 * np.pi * 9 * T(.6))), t + 2.6, .2, .3, .1)   # wobble
m.whoosh(t + 3.35, .35, .3, False, .3); m.thud(t + 3.7, .8, .3); for_ = [clink(t + 3.75 + k * .07, .2, 900 + k * 80) for k in range(5)]; m.tweet(t + 3.85, 3, .12, .3)
m.f(m.wav('laugh_crowd'), t + 3.8, .3, 0, .3)
# EXHIBIT 2: UCL cups as dumbbells
t = S['ucl']; stinger(t, ['F3', 'C4', 'F4'])
for k in range(5): clink(t + .4 + k * .4, .25, 1800); voice(t + .4 + k * .4, .2, 140, 190, .25, .3)
m.f(m.wav('siu'), t + 2.8, .9, .2, .25); m.cheer_burst(t + 2.9, .3)
# EXHIBIT 3: World Cup
t = S['wc']; stinger(t, ['G3', 'D4', 'G4']); choir(t + .5, 2.0); m.harp_gliss(t + .45, ['D4', 'F#4', 'A4', 'D5', 'F#5', 'A5'], .06); m.sparkle(t + .6, .9, .12)
m.pop(t + 1.2, .3, 1200); m.ding(t + 1.45, 2637, .2)   # sunglasses on
m.f(m.wav('cheer_crowd'), t + .9, .3, -.3, .3)
# EXHIBIT 4: ball machine flood
t = S['intl']; stinger(t, ['A2', 'E3', 'A3'])
m.f(lp(osc(55, 3.2, 'saw'), 300) * env(int(3.2 * SR), .2, .3) * .5, t + .5, .3, .4, .1)   # motor
for k in range(30): m.pop(t + .5 + k * .09, .2, 500 + (k % 5) * 120, .4)
voice(t + 1.6, .6, 300, 420, .35, -.3, 600, 1800)
# EXHIBIT 5: assists scroll vs 4 countries -> OBJECTION
t = S['assist']; stinger(t, ['C3', 'G3', 'C4'])
m.f(bp(noise(1.4), 1500, 6000) * env(int(1.4 * SR), .05, .3) * .5, t + .05, .3, -.2, .1)   # paper unrolling
for k in range(4): m.pop(t + 1.45 + k * .1, .25, 800 + k * 150)
mumble(t + 2.6, 5, 480, .35, -.3); mumble(t + 2.8, 5, 360, .35, .3); gavel(t + 3.3, .6)
# VERDICT
t = S['verdict']; m.f(osc(glide(80, 50, .8), .8) * env(int(.8 * SR), .3, .2) * .4, t, .3, 0, .3)
chew(t + .5, 1.4); burp(t + 1.75); m.f(m.wav('laugh_crowd'), t + 1.9, .35, 0, .3)
m.thud(t + 2.1, 1.0); gavel(t + 2.1, .8); m.brass_hit([hz('D3'), hz('F3'), hz('A3'), hz('D4')], t + 2.15, .9, .28)
# THANKS
t = S['thanks']
for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'G5', 'E5', 'C6']): m.pluck(hz(n), t + .1 + i * .18, .6, .2, -.3 + i * .1, .5, .4)
m.saw_chord([hz('C4'), hz('E4'), hz('G4')], t + .1, 2.6, .05, 1600, 0, .3, .8, .4)
m.ding(t + 1.2, 2093, .35); m.pop(t + 1.2, .3); bleat(t + 1.6, .3)
m.write(sys.argv[1])
