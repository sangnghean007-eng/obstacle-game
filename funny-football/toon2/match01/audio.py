"""MATCH 01 sound: stadium drums + crowd (new style), goal horns and roars, half-time hum, extra-time heartbeat, penalty whistles. vox2/fx2 only."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
G0 = 2.5; EV = [(3.0, 'W'), (5.6, 'W'), (6.6, 'W'), (12.0, 'R'), (13.5, 'R'), (15.0, 'R')]
P0 = G0 + 18.1; PST = .95; PENS = [('W', 0, 'over'), ('R', 1, ''), ('W', 0, 'saved'), ('R', 1, ''), ('W', 1, ''), ('R', 0, 'saved'), ('W', 1, ''), ('R', 1, ''), ('W', 0, 'saved')]
END = P0 + 9 * PST + 1.6 + 4.6; m = Mix2(END, ep=201)
def drums(t0, t1, g=.6, bpm=96):
    b = 60 / bpm; t = t0; i = 0
    while t < t1 - .02:
        m.timpani(t, 70 if i % 4 == 0 else 95, .25 * g) if i % 2 == 0 else m.clap(t, .12 * g); t += b / 2; i += 1
def whistle(t, n=1, g=.35):
    for k in range(n): d = .25 if n > 1 else .5; tt = T(d); m.f(osc(2800 * (1 + .03 * np.sin(2 * np.pi * 40 * tt)), d) * env(len(tt), .01, .03), t + k * .32, g, 0, .2)
def roar(t, g=.45, d=2.2): m.crowd(t, 'cheer', d, g); m.f(bp(noise(d), 200, 2500) * env(int(d * SR), .05, 1.0), t, g * .6, 0, .3)
def horn(t, g=.3): d = .9; tt = T(d); m.f(bp(osc(233, d, 'saw') + osc(311, d, 'saw'), 200, 1800) * env(len(tt), .02, .2), t, g)
m.f(bp(noise(END), 300, 1800) * .25, 0, .25, 0, .1)  # stadium bed
m.timpani(.05, 80, .5, roll=.4); m.xylo_rise(.1, .12); whistle(G0 + .1)
drums(G0, G0 + 5.5, .6)
for t, tm in EV:
    m.slide_whistle(G0 + t - 2.5 - .5, True, .45, .15); m.thump(G0 + t - 2.5, .7); horn(G0 + t - 2.5 + .05); roar(G0 + t - 2.5 + .05, .5 if tm == 'R' else .35, 2.0)
    if tm == 'W': m.vo('generic_m', 'no', G0 + t - 2.5 + .3, .4, -.4)
    else: m.vo('generic_m', 'yay', G0 + t - 2.5 + .2, .5, -.3)
whistle(G0 + 5.5, 2)  # half-time
for i in range(8): m.vo(['generic_m', 'generic_f', 'big', 'generic_m'][i % 4], 'hmm', G0 + 6.2 + i * .2, .25, -.5 + i * .12)  # the red end hums through half-time
m.kazoo(G0 + 6.4, ['C4', None, 'D4', 'E4', None, 'E4'], .32, .08)
whistle(G0 + 8.05); drums(G0 + 8.1, G0 + 13.5, .85, 112)
m.heartbeat(G0 + 14.3, .5); m.heartbeat(G0 + 15.1, .5); m.whoosh(G0 + 15.5, .4, .3); m.smack(G0 + 15.6, .6); m.smack(G0 + 15.9, .6); m.crowd(G0 + 15.7, 'gasp', 1.2, .4)
whistle(G0 + 16.9, 3)
for k in range(9):
    tm, ok, how = PENS[k]; t = P0 + k * PST; m.heartbeat(t, .35); whistle(t + .15, 1, .25); m.thwack(t + .5, .7)
    if ok: m.thump(t + .55, .5); roar(t + .6, .35 if tm == 'R' else .25, 1.0)
    elif how == 'saved': m.smack(t + .55, .7); m.crowd(t + .6, 'gasp', .8, .35)
    else: m.slide_whistle(t + .5, True, .5, .25); m.crowd(t + .6, 'gasp', .8, .3)
t = P0 + 9 * PST; roar(t, .6, 3.5); m.firework(t + .3, .3); m.firework(t + .8, .3, .4); m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t + .1, 1.2, .25)
m.kazoo(END - 3.5, ['G4', 'A4', 'B4', 'D5'], .2, .12); m.vo('generic_m', 'hmm', END - 2.6, .45)
m.write(sys.argv[1])
