"""Ep8 ROAD TO 1000 sound: adventure-trap bed, wind, climbing foley, a drumroll + airhorn + roar on every goal, goat bleats. No TTS."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(open=0, title=2.6, climb=4.8, intro=9.2, g1=11.8, g2=16.4, g3=21.0, topper=26.0, twist=30.4, thanks=33.4); END = 36.8
m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def bed(t0, t1, g=1.0, bpm=100):  # original heroic adventure trap: brass chords + 808 + hats
    b = 60 / bpm; t = t0; i = 0; prog = [['E3', 'G3', 'B3'], ['C3', 'E3', 'G3'], ['D3', 'F#3', 'A3'], ['B2', 'D#3', 'F#3']]
    while t < t1 - .05:
        m.saw_chord([hz(n) for n in prog[i % 4]], t, 4 * b * .95, .06 * g, 1500, 0, .2, .3, .4)
        for k in (0, 1.5, 2.5): k808(t + k * b, .7 * g)
        for k in (1, 3): m.clap(t + k * b, .33 * g)
        for k in range(16 if i % 2 else 8): m.hat(t + k * b / (4 if i % 2 else 2), .07 * g, False, .3)
        m.pluck(hz(['E5', 'G5', 'F#5', 'D#5'][i % 4]), t + 3.5 * b, .3, .12 * g, .3, .9, .3)
        t += 4 * b; i += 1
def wind(t, d, g=.12): m.f(bp(noise(d), 300, 1200) * env(int(d * SR), .5, .8) * (1 + .5 * np.sin(2 * np.pi * .4 * T(d))), t, g, 0, .2)
def drumroll(t, d=.5): [m.snare(t + k * d / 20, .12 + .25 * k / 20, (k % 2) * .2 - .1) for k in range(20)]
def airhorn(t, g=.32): d = .7; x = sum(osc(f * (1 + det), d, 'saw') for f in (hz('A4'), hz('C#5'), hz('E5')) for det in (-.004, .004)); m.f(lp(x, 4500) * env(int(d * SR), .01, .2), t, g, 0, .2)
def bleat(t, g=.4, f0=520): d = .6; tt = T(d); f = f0 * (1 + .12 * np.sign(np.sin(2 * np.pi * 14 * tt))); m.put(m.vox, bp(osc(f, d, 'saw'), 600, 2600) * env(int(d * SR), .03, .15), t, g, 0, .1)
def chew(t, d=1.0, g=.28): [m.f(bp(noise(.06), 800, 4000) * dec(.06, 50), t + k * .11, g, 0, .05) for k in range(int(d / .11))]
def grunt(t, g=.35, f0=150, f1=110, d=.3): tt = T(d); x = osc(glide(f0, f1, d), d, 'saw'); m.put(m.vox, bp(x, 300, 1400) * env(len(tt), .02, .1), t, g, -.1, .05)
def roar(t, g=.45): m.crowd(t, 2.0, g); m.f(m.wav('cheer_crowd'), t + .05, g * .9, 0, .25)
def ticks(t0, t1, step=.5):
    t = t0
    while t < t1: m.tick(t, True, .14); t += step

wind(0, END - 3.4, .1)
# OPEN: boom on frame 0, scramble, goat laugh
m.kick(0, 1.0); m.thud(0, .9); m.crash(0, .4); m.brass_hit([hz('E3'), hz('B3'), hz('E4')], 0, .6, .3)
for k in range(6): m.footstep(.2 + k * .17, .25, .2)
grunt(.4); grunt(.9, .3, 170, 120); bleat(1.0, .45, 600); m.f(m.wav('laugh_crowd'), 1.1, .25, 0, .3)
# TITLE
m.whoosh(S['title'], .5, .45, False); m.brass_hit([hz('E3'), hz('G#3'), hz('B3'), hz('E4')], S['title'] + .4, .9, .32); m.crash(S['title'] + .4, .35)
bed(S['title'] + .4, S['topper'] + .1, .9)
# CLIMB montage: fast climbing foley + odometer ticks, goat slurp
t = S['climb']
for k in range(28): m.footstep(t + .15 + k * .14, .22, (-1) ** k * .3)
for k in range(9): m.pop(t + .5 + k * .38, .18, 900 + k * 90)
m.slurp(t + 1.4, .8, .25, .3); grunt(t + 2.6, .3, 160, 120, .4); grunt(t + 3.3, .3, 180, 130, .4); m.thud(t + 4.1, .5)
# INTRO: date stamp, stopwatch click, ball drop
t = S['intro']; m.thud(t, .6); m.brass_hit([hz('B2'), hz('F#3'), hz('B3')], t, .5, .25)
m.ding(t + .5, 2637, .2); m.tick(t + 1.6, True, .3); ticks(t + 1.6, S['topper'], .5)
for k in range(4): m.pop(t + .2 + k * .2, .2, 300)
m.whoosh(t + 1.4, .35, .3, False); m.bonk(t + 1.8, .5); bleat(t + .8, .25, 480)
# GOALS: wind-up, kick, drumroll, NET, airhorn + roar, travel sound, landing
for i, g in enumerate(['g1', 'g2', 'g3']):
    t = S[g]
    grunt(t + .4, .3); m.thwack(t + .62, .9); m.whoosh(t + .62, .4, .35, True, .3); drumroll(t + .62, .48)
    tn = t + 1.1; m.net(tn, .7); k808(tn, 1.0); m.crash(tn, .45); airhorn(tn + .02); roar(tn + .05, .45)
    [m.ding(tn + .15 + j * .1, f, .18, -.3) for j, f in enumerate([1568, 1976, 2349, 3136])]
    if i == 0: m.snore(t + 1.2, .7, .2); bleat(t + 2.0, .3, 500)
    if i == 1: m.boing(t + .9, .35, .4, 300, 160); m.f(m.wav('ooh_crowd'), t + 1.3, .3, 0, .3); m.boing(t + 1.55, .55, .5)
    if i == 2: m.bonk(t + 1.12, .6); m.tweet(t + 1.3, 4, .14, .3)
    m.whoosh(t + 1.7, .8, .4, True)
    if i == 2: m.f(lp(noise(.9), 900) * env(int(.9 * SR), .05, .3), t + 1.7, .35, 0, .1)
    m.thud(t + 2.6, .7)
    if i == 2: m.f(m.wav('siu'), t + 2.65, 1.0, .2, .25); m.f(m.wav('siu_crowd'), t + 2.9, .5, 0, .3); m.firework(t + 3.0, .3, -.3); m.firework(t + 3.3, .3, .3)
    else: m.f(m.wav('chuckle'), t + 2.8, .35, 0, .1)
# TOPPER: gulp, pull back to the summit, chomp, angry
t = S['topper']; m.slowdown(t + .7, .8, .3); m.brass_hit([hz('E3'), hz('A#3'), hz('E4')], t + 1.2, .8, .3); m.f(m.wav('gasp'), t + .8, .4, 0, .2)
m.whoosh(t + 2.0, .4, .35, True); bleat(t + 2.2, .4, 560); chew(t + 2.3, .7, .35); m.bonk(t + 2.5, .3)
m.scratch(t + 2.9, .4); m.f(m.wav('grumble_angry'), t + 3.15, .45, 0, .1); m.kettle(t + 3.2, 1.0, .14)
# TWIST: charge
t = S['twist']; bed(t, S['thanks'] + .05, 1.0, 120)
for k in range(18): m.footstep(t + k * .1, .3, (-1) ** k * .3)
m.whoosh(t + .1, .6, .4, True); bleat(t + .4, .4, 650); grunt(t + .6, .4, 200, 150, .5); m.brass_hit([hz('E3'), hz('B3'), hz('E4'), hz('G4')], t + .6, .8, .3)
# THANKS
t = S['thanks']
for i, n in enumerate(['E5', 'G5', 'B5', 'E6', 'B5', 'G5', 'E6']): m.pluck(hz(n), t + .1 + i * .18, .6, .22, -.3 + i * .1, .5, .4)
m.saw_chord([hz('E4'), hz('G4'), hz('B4')], t + .1, 3.1, .05, 1600, 0, .3, .8, .4); m.ding(t + 1.2, 2093, .35); m.pop(t + 1.2, .3); bleat(t + 2.0, .3); chew(t + 2.3, .8, .2)
m.write(sys.argv[1])
