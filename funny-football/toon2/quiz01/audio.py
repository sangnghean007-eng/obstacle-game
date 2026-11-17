"""QUIZ 01 sound: game-show synth (new style), tile whooshes with rising plucks, ticking clock, reveal fanfare + crowd. vox2/fx2 only, no stock WAVs."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
ARR, THINK = .55, 3.5
R0 = [2.2, 11.10, 19.45]; NCL = [6, 5, 6]; END = 31.35; m = Mix2(END, ep=101)
def gameshow(t0, t1, g=.6, bpm=128, root='A'):
    b = 60 / bpm; t = t0; i = 0; arp = ['A3', 'C4', 'E4', 'A4', 'E4', 'C4', 'G3', 'B3', 'D4', 'G4', 'D4', 'B3']
    while t < t1 - .02:
        m.pluck(hz(arp[i % 12]), t, b * .45, .1 * g, .3, 1.4)
        if i % 4 == 0: m.kick(t, .3 * g)
        if i % 4 == 2: m.clap(t, .12 * g)
        m.hat(t + b / 4, .03 * g); t += b / 2; i += 1
# INTRO: sting
m.brass_hit([hz('A3'), hz('C#4'), hz('E4')], 0.05, .5, .22); m.xylo_rise(.1, .15); m.crowd(.3, 'gasp', 1.0, .15)
for r, (t0, n) in enumerate(zip(R0, NCL)):
    tEnd = t0 + .2 + n * ARR; rev = tEnd + THINK
    gameshow(t0, tEnd, .7 + .1 * r)
    m.f(osc(glide(300, 900, .25), .25) * env(int(.25 * SR), .01, .1), t0, .2)  # level sting
    for j in range(n): m.whoosh(t0 + .2 + j * ARR, .25, .18, True, -.3); m.pluck(hz(['C5', 'D5', 'E5', 'F5', 'G5', 'A5'][j]), t0 + .25 + j * ARR, .2, .18, .2)
    for k in range(int(THINK / .5)): m.tick(tEnd + k * .5, k % 2 == 0, .35 + k * .03)
    m.timpani(rev - .7, 82, .4, roll=.6)
    m.brass_hit([hz('D4'), hz('F#4'), hz('A4'), hz('D5')], rev, .8, .25); m.xylo_rise(rev + .05, .15); m.crowd(rev + .1, 'cheer', 1.6, .3); m.cork(rev, .3)
    m.vo(['ronaldo', 'haaland', 'kane'][r], ['siu', 'yay', 'yay'][r], rev + .25, .6)
# OUTRO
m.kazoo(R0[2] + .2 + 6 * ARR + THINK + 1.9 + .2, ['C5', 'E5', 'G5', 'C6'], .16, .14); m.crowd(END - 2.6, 'laugh', 2.0, .2)
m.write(sys.argv[1])
