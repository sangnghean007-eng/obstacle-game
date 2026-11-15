"""Ep10 FINAL FIGHT sound: fighting-game arcade score, round gongs, whooshes per special move, heavy hits, crowd, SIUUU. No TTS."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
RD, HIT = 3.8, 2.0
R0 = 2.0; S = dict(draw=2.0 + 6 * RD, final=2.0 + 6 * RD + 1.4, thanks=2.0 + 6 * RD + 1.4 + 3.6); END = S['thanks'] + 2.8
m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def arcade(t0, t1, g=1.0, bpm=140):  # original arcade fight loop: driving bass + stabs + hats
    b = 60 / bpm; t = t0; i = 0; roots = ['E2', 'E2', 'G2', 'A2', 'E2', 'E2', 'D2', 'B1']
    while t < t1 - .05:
        r = roots[i % 8]
        for k in range(4): m.bass(hz(r) * (2 if k % 2 else 1), t + k * b * .5, b * .45, .3 * g)
        k808(t, .6 * g); m.snare(t + b, .25 * g); m.hat(t + b * .5, .08 * g); m.hat(t + b * 1.5, .08 * g)
        if i % 2 == 0: m.saw_chord([hz('E4'), hz('G4'), hz('B4')], t, b * .25, .05 * g, 2500, 0, .005, .05, .2)
        t += 2 * b; i += 1
def gong(t, g=.5): d = 2.0; x = sum(a * osc(f, d) for f, a in [(110, 1), (163, .6), (247, .4), (330, .3)]) * dec(d, 1.6); m.f(x, t, g, 0, .4)
def hit(t, g=1.0): k808(t, g); m.thud(t, .9 * g); m.crash(t, .4); m.f(bp(noise(.12), 1500, 6000) * dec(.12, 30), t, .6 * g, 0, .2)
# HOOK: VS slam
hit(0, 1.0); gong(0, .4); m.brass_hit([hz('E3'), hz('B3'), hz('E4')], 0, .8, .35); m.crowd(0, 2.0, .3)
arcade(R0 - 0.1, S['draw'], .85)
m.crowd(R0, S['draw'] - R0, .14, swell=False)
moves = ['ballon', 'ucl', 'beam', 'kick', 'assist', 'siu']; wins = 'MRMRMR'
for i in range(6):
    t = R0 + i * RD; gong(t, .35); m.pop(t + .6, .25, 1200); m.pop(t + .72, .25, 1500)
    th = t + HIT
    if moves[i] == 'ballon': [m.ding(th - .6 + j * .07, 1800 + j * 120, .12, .3) for j in range(8)]; m.whoosh(th - .6, .6, .35, True)
    if moves[i] == 'ucl': [m.whoosh(th - .6 + j * .1, .3, .2, True, -.3 + j * .15) for j in range(5)]
    if moves[i] == 'beam': m.choir([hz('E4'), hz('G#4'), hz('B4'), hz('E5')], th - .7, .8, .2); m.f(lp(osc(glide(200, 900, .6), .6, 'saw'), 2500) * env(int(.6 * SR), .05, .1), th - .6, .25, 0, .2)
    if moves[i] == 'kick': [m.thwack(th - .6 + j * .06, .45, -.3 + j * .07) for j in range(9)]
    if moves[i] == 'assist': m.thwack(th - .6, .6); m.whoosh(th - .5, .5, .35, False); m.boing(th - .05, .4)
    if moves[i] == 'siu': m.f(m.wav('siu'), th - .55, 1.0, -.2, .25); m.f(lp(noise(.8), 400) * env(int(.8 * SR), .01, .5), th - .3, .5, 0, .2)
    hit(th); m.cheer_burst(th + .05, .4)
    m.f(m.wav('gasp' if wins[i] == 'R' else 'grumble_angry'), th + .6, .3, .3 if wins[i] == 'R' else -.3, .1)
    if wins[i] == 'R' and moves[i] != 'siu': m.f(m.wav('siu'), th + .35, .6, -.3, .25)
t = S['draw']; hit(t, 1.0); m.slowdown(t + .1, .8, .4); m.brass_hit([hz('D3'), hz('G#3'), hz('D4')], t + .2, .9, .35); m.f(m.wav('ooh_crowd'), t + .2, .4, 0, .3)
t = S['final']; gong(t, .45); m.drone(hz('E2'), t, 3.5, .12)
for j in range(16): m.tick(t + .4 + j * .075, j % 2 == 0, .18)
m.ding(t + 1.6, 2093, .3); m.ding(t + 1.75, 2637, .3); m.f(m.wav('bleat'), t + 1.9, .3, .4, .1); m.brass_hit([hz('E3'), hz('B3'), hz('E4'), hz('G4')], t + 2.1, .8, .32)
t = S['thanks']
for i, n in enumerate(['E5', 'G5', 'B5', 'E6', 'B5', 'G5', 'E6']): m.pluck(hz(n), t + .1 + i * .16, .6, .22, -.3 + i * .1, .5, .4)
m.ding(t + 1.0, 2093, .35); m.pop(t + 1.0, .3)
m.write(sys.argv[1])
