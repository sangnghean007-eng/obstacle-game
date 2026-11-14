"""Ep7 v3 GOAT COURT sound: driving courtroom-trap score, drumrolls, winner airhorns + crowd roars, loser wah-wah. No TTS."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

EX = 5.6; WIN = 2.6
S = dict(open=0, e1=2.6, verdict=2.6 + 6 * EX, thanks=2.6 + 6 * EX + 4.6); END = 2.6 + 6 * EX + 4.6 + 3.0
EXH = [(2.6 + i * EX, w) for i, w in enumerate('MRMRMR')]
m = Mix(END)
def voice(t, d, f0, f1, g=.4, pan=0, lo=500, hi=1600, buzz=1.0):
    tt = T(d); f = glide(f0, f1, d) * (1 + .03 * np.sin(2 * np.pi * 7 * tt)); x = osc(f, d, 'saw') * buzz + .3 * osc(f * 2, d)
    y = bp(x, lo, hi) + .4 * bp(x, hi * 1.6, hi * 2.2); y *= env(len(y), .03, .1) * (1 + .3 * np.sin(2 * np.pi * 11 * tt)); m.put(m.vox, y, t, g, pan, .03)
def mumble(t, n, f0, g=.3, pan=0):
    R = np.random.default_rng(int(t * 100))
    for i in range(n): f = f0 * (1 + R.uniform(-.25, .3)); d = .07 + R.random() * .04; x = bp(osc(f, d, 'saw'), 500, 2500) * env(int(d * SR), .005, .03); m.put(m.vox, x, t + i * .1, g, pan, .02)
def gavel(t, g=.9): m.f(bp(noise(.15), 300, 2500) * dec(.15, 40) + osc(glide(220, 120, .15), .15) * dec(.15, 30), t, g, 0, .5)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def trap(t0, t1, g=1.0, bpm=96):  # original courtroom trap: strings + 808 + rolling hats
    b = 60 / bpm; t = t0; i = 0; prog = [['D3', 'F3', 'A3'], ['A#2', 'D3', 'F3'], ['C3', 'E3', 'G3'], ['A2', 'C#3', 'E3']]
    while t < t1 - .05:
        m.saw_chord([hz(n) for n in prog[i % 4]], t, 4 * b * .95, .06 * g, 1400, 0, .2, .3, .4)
        for k in (0, 1.5, 2.5): k808(t + k * b, .7 * g)
        for k in (1, 3): m.clap(t + k * b, .35 * g)
        for k in range(16 if i % 2 else 8): m.hat(t + k * b / (4 if i % 2 else 2), .07 * g, False, .3)
        m.pluck(hz(['D5', 'F5', 'E5', 'C#5'][i % 4]), t + 3.5 * b, .3, .12 * g, .3, .9, .3)
        t += 4 * b; i += 1
def drumroll(t, d=.6): [m.snare(t + k * d / 24, .12 + .25 * k / 24, (k % 2) * .2 - .1) for k in range(24)]
def airhorn(t, g=.32): d = .7; x = sum(osc(f * (1 + det), d, 'saw') for f in (hz('A4'), hz('C#5'), hz('E5')) for det in (-.004, .004)); m.f(lp(x, 4500) * env(int(d * SR), .01, .2), t, g, 0, .2); m.f(lp(x, 4500) * env(int(.3 * SR), .01, .1)[:int(.3 * SR)] if False else lp(sum(osc(f, .3, 'saw') for f in (hz('A4'), hz('C#5'))), 4500) * env(int(.3 * SR), .01, .1), t + .8, g * .8, 0, .2)
def wahwah(t, g=.22):
    for i, (n, d) in enumerate([('D3', .25), ('C#3', .25), ('C3', .5)]): tt = T(d); f = hz(n) * (1 + .015 * np.sin(2 * np.pi * 6 * tt)); m.m(lp(osc(f, d, 'saw'), 900) * env(len(tt), .02, .08), t + i * .28, g, .3, .3)
def clink(t, g=.3, f=1500): d = .5; x = sum(a * osc(f * k, d) for k, a in [(1, 1), (2.7, .5), (5.2, .25)]) * dec(d, 9); m.f(x, t, g, np.random.uniform(-.4, .4), .3)
def bleat(t, g=.4): d = .6; tt = T(d); f = 520 * (1 + .12 * np.sign(np.sin(2 * np.pi * 14 * tt))); m.put(m.vox, bp(osc(f, d, 'saw'), 600, 2600) * env(int(d * SR), .03, .15), t, g, 0, .1)
def chew(t, d=1.4): [m.f(bp(noise(.06), 800, 4000) * dec(.06, 50), t + k * .11, .28, 0, .05) for k in range(int(d / .11))]
def stinger(t, notes, g=.24): m.brass_hit([hz(n) for n in notes], t, .5, g)
def roar(t, g=.45): m.crowd(t, 2.2, g); m.f(m.wav('cheer_crowd'), t + .05, g * .9, 0, .25)

m.crowd(0, S['thanks'], .1, swell=False)
# OPEN
gavel(.25); gavel(.65); bleat(.9, .4); m.f(m.wav('ooh_crowd'), .9, .3, 0, .3)
for k in range(8): m.footstep(1.0 + k * .07, .28, -.6 + k * .17)
m.f(osc(glide(3000, 3400, .4), .4) * .2 * env(int(.4 * SR), .02, .1), 1.6, .18, 0, .1)
trap(1.4, S['verdict'] - .1, .9)
# EXHIBITS: present -> drumroll -> WIN (airhorn, roar, signature) -> loser wah-wah
props = [  # presentation foley per exhibit
  lambda t: ([clink(t + i * .16, .22, 1300 + i * 110) for i in range(8)], [clink(t + .4 + i * .22, .2, 1000 + i * 90) for i in range(5)], voice(t + 1.4, .5, 160, 230, .35, .3)),
  lambda t: [ (clink(t + .3 + k * .4, .25, 1800), voice(t + .3 + k * .4, .2, 140, 190, .25, .3)) for k in range(5)],
  lambda t: (m.choir([hz('D4'), hz('F#4'), hz('A4'), hz('D5')], t + .5, 2.0, .2), m.harp_gliss(t + .45, ['D4', 'F#4', 'A4', 'D5', 'F#5', 'A5'], .06), m.pop(t + 1.25, .3, 1200), m.ding(t + 1.5, 2637, .2)),
  lambda t: (m.f(lp(osc(55, 2.2, 'saw'), 300) * env(int(2.2 * SR), .2, .3) * .5, t + .4, .3, .4, .1), [m.pop(t + .4 + k * .08, .2, 500 + (k % 5) * 120, .4) for k in range(26)]),
  lambda t: (m.f(bp(noise(1.6), 1500, 6000) * env(int(1.6 * SR), .05, .3) * .5, t + .05, .3, -.2, .1), voice(t + 1.0, .4, 300, 260, .3, .3, 600, 1800)),
  lambda t: [m.pop(t + .35 + k * .1, .25, 800 + k * 150) for k in range(4)],
]
for i, (t, w) in enumerate(EXH):
    stinger(t, [['D3', 'A3', 'D4'], ['F3', 'C4', 'F4'], ['G3', 'D4', 'G4'], ['A2', 'E3', 'A3'], ['C3', 'G3', 'C4'], ['E3', 'B3', 'E4']][i])
    props[i](t)
    drumroll(t + WIN - .6); tw = t + WIN
    gavel(tw, .8); k808(tw, 1.0); m.crash(tw, .45); airhorn(tw + .02); roar(tw + .05, .45)
    if w == 'R': m.f(m.wav('siu'), tw + .15, .95, .3, .25); m.whoosh(tw + .05, .5, .3, True, .3)
    else: m.sparkle(tw + .1, .6, .14); [m.ding(tw + .1 + j * .12, f, .22, -.3) for j, f in enumerate([1568, 1976, 2349, 3136])]
    wahwah(tw + .9, .2)
    if i == 0: m.thud(tw + .55, .7, .3); m.tweet(tw + .7, 3, .12, .3)
    if i in (4, 5): [m.thud(tw + .3 + k * .25, .4, -.3 if w == 'R' else .3) for k in range(4)]; m.kettle(tw + .3, .8, .12)
# VERDICT
t = S['verdict']; drumroll(t, .5); m.brass_hit([hz('D3'), hz('G#3'), hz('D4')], t + .5, .7, .3); m.f(m.wav('ooh_crowd'), t + .4, .4, 0, .3)
bleat(t + 1.1, .4); chew(t + 1.3, 1.4); voice(t + 2.5, .5, 110, 80, .5, 0, 150, 600); m.f(m.wav('laugh_crowd'), t + 2.6, .4, 0, .3)
m.thud(t + 2.9, 1.0); gavel(t + 2.9, .9); m.brass_hit([hz('D3'), hz('F3'), hz('A3'), hz('D4')], t + 2.95, .9, .3); m.crash(t + 2.95, .35)
# THANKS
t = S['thanks']
for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'G5', 'E5', 'C6']): m.pluck(hz(n), t + .1 + i * .18, .6, .22, -.3 + i * .1, .5, .4)
m.saw_chord([hz('C4'), hz('E4'), hz('G4')], t + .1, 2.8, .05, 1600, 0, .3, .8, .4); m.ding(t + 1.2, 2093, .35); m.pop(t + 1.2, .3); bleat(t + 1.8, .3)
m.write(sys.argv[1])
