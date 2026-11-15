"""Ep10 v5 GOAT GAMES sound: a different chiptune/game sound-world per game. Original synth only, no TTS."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
T = dict(select=2.0, r1=3.3, kart=6.7, jump=10.3, shooter=13.7, pinball=17.0, quiz=20.4, boss=27.2, draw=31.2, thanks=32.6); END = 35.4
m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def sq(f, t, d, g=.12, pan=0): m.m(lp(osc(f, d, 'sq'), 3500) * env(int(d * SR), .005, .03), t, g, pan, .05)
def chip(t0, t1, notes, step, g=.12, bass=None):
    t = t0; i = 0
    while t < t1 - .02:
        sq(hz(notes[i % len(notes)]), t, step * .9, g)
        if bass and i % 2 == 0: m.bass(hz(bass[(i // 2) % len(bass)]), t, step * 1.8, .25)
        if i % 2 == 0: m.hat(t, .05)
        if i % 4 == 0: k808(t, .5)
        t += step; i += 1
def coin(t, g=.25): sq(hz('B5'), t, .06, g); sq(hz('E6'), t + .06, .18, g)
def hit(t, g=1.0): k808(t, g); m.thud(t, .8 * g); m.crash(t, .35)
def jingle(t, up=True): [sq(hz(n), t + i * .08, .1, .16) for i, n in enumerate(['C5', 'E5', 'G5', 'C6'] if up else ['G4', 'E4', 'C4'])]
# hook + select
hit(0); m.brass_hit([hz('E3'), hz('B3'), hz('E4')], 0, .8, .35); m.crowd(0, 2.0, .3)
for i in range(10): sq(hz(['C5', 'E5', 'G5', 'E5'][i % 4]), T['select'] + i * .12, .08, .12)
coin(T['select'] + 1.15)
# G1 fight (Ballon d'Or combo)
t = T['r1']; m.gong = None; [m.ding(t + 1.2 + j * .075, 1800 + j * 120, .16, .3) for j in range(8)]; m.whoosh(t + 1.2, .6, .35, True); hit(t + 1.8); m.cheer_burst(t + 1.85, .4)
chip(t, t + 3.4, ['E4', 'G4', 'B4', 'G4'], .14, .08, ['E2', 'D2'])
# G2 kart: engine drone + item pickups
t = T['kart']; m.f(lp(osc(glide(80, 140, 3.4), 3.4, 'saw'), 600) * env(int(3.4 * SR), .1, .3), t, .18, 0, .05)
chip(t, t + 3.6, ['A4', 'C5', 'E5', 'C5', 'D5', 'F5'], .12, .1, ['A2', 'F2'])
for x in [.4, .9, 1.4, 1.9, 2.4, .6, 1.1, 1.6, 2.1]: coin(t + x, .18)
jingle(t + 3.0); m.cheer_burst(t + 3.05, .35)
# G3 jump: boing jumps, block hits
t = T['jump']; chip(t, t + 3.4, ['C5', 'C5', 'G4', 'E4', 'A4', 'B4'], .13, .1, ['C3', 'G2'])
for x in [0, .6, 1.2, 1.8]: m.boing(t + x, .25, .3, 300, 700)
m.bonk(t + 2.0, .4); jingle(t + 2.05); m.choir([hz('C5'), hz('E5'), hz('G5')], t + 2.1, .7, .14); m.bonk(t + 2.3, .5); m.tweet(t + 2.4, 3, .12)
# G4 shooter: laser pews + counter ticks
t = T['shooter']; chip(t, t + 3.3, ['E5', 'E5', 'D5', 'E5', 'G5', 'E5'], .1, .09, ['E2'])
for j in range(26): m.f(osc(glide(1800, 600, .08), .08, 'sq') * dec(.08, 30), t + .5 + j * .09, .08, -.3 if j % 2 else .3, .02)
jingle(t + 2.8); m.cheer_burst(t + 2.85, .35)
# G5 pinball: bumper dings + flipper clacks
t = T['pinball']; chip(t, t + 3.4, ['G4', 'B4', 'D5', 'B4'], .11, .09, ['G2', 'D2'])
for j in range(7): m.ding(t + j * .4, 1200 + j * 150, .22, -.3 + j * .1)
m.f(bp(noise(.05), 800, 3000) * dec(.05, 60), t + .05, .5); m.f(bp(noise(.05), 800, 3000) * dec(.05, 60), t + 2.6, .5); m.f(m.wav('grumble_angry'), t + 2.7, .3, .3, .1); jingle(t + 2.9)
# G6 quiz: buzzers per card
t = T['quiz']; m.saw_chord([hz('C4'), hz('E4'), hz('G4')], t, 6.8, .04, 1600, 0, .3, .5, .4)
for j in range(8): tb = t + j * .85; m.pop(tb, .2, 1200); m.f(lp(osc(glide(180, 170, .35), .35, 'sq'), 1200) * env(int(.35 * SR), .005, .05), tb + .22, .25, .4 if j % 2 == 0 else -.4, .02); m.ding(tb + .3, 2093, .15)
m.f(m.wav('ooh_crowd'), t + 6.3, .35, 0, .3)
# G7 boss: rumble, SIUUU blast, free-kick volley, bleat
t = T['boss']; m.drone(hz('A1'), t, 4.0, .18); m.f(m.wav('bleat'), t + .2, .4, 0, .2); m.f(m.wav('siu'), t + .7, 1.0, -.3, .25); hit(t + .8, .9)
[m.thwack(t + 1.9 + j * .08, .45, .3) for j in range(4)]; hit(t + 2.3, .8); m.brass_hit([hz('A2'), hz('E3'), hz('A3')], t + 2.9, .8, .3)
# draw + thanks
t = T['draw']; hit(t); m.slowdown(t + .1, .8, .4); m.f(m.wav('ooh_crowd'), t + .2, .4, 0, .3)
t = T['thanks']
for i, n in enumerate(['E5', 'G5', 'B5', 'E6', 'B5', 'G5', 'E6']): m.pluck(hz(n), t + .1 + i * .16, .6, .22, -.3 + i * .1, .5, .4)
m.ding(t + 1.0, 2093, .35); m.pop(t + 1.0, .3)
m.write(sys.argv[1])
