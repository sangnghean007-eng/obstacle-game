"""Ep9 NO RONALDO, NO PROBLEM? sound: bright 'how it started' groove, sad 'how it's going' groove, drumroll + Danish horn + roar per goal, wah-wah for Portugal. No TTS."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(hook=0, started=2.6, press=4.1, oct=8.7, retire=13.5, going=16.7, tribute=18.2, g1=21.0, g2=25.8, g3=30.7, g4=35.7, consol=40.9, twist=43.7, thanks=47.9); END = 51.3
m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def groove(t0, t1, prog, lead, g=1.0, bpm=104):
    b = 60 / bpm; t = t0; i = 0
    while t < t1 - .05:
        m.saw_chord([hz(n) for n in prog[i % len(prog)]], t, 4 * b * .95, .055 * g, 1500, 0, .2, .3, .4)
        for k in (0, 1.5, 2.5): k808(t + k * b, .65 * g)
        for k in (1, 3): m.clap(t + k * b, .3 * g)
        for k in range(8): m.hat(t + k * b / 2, .07 * g, False, .3)
        m.pluck(hz(lead[i % len(lead)]), t + 3.5 * b, .3, .12 * g, .3, .9, .3)
        t += 4 * b; i += 1
def drumroll(t, d=.5): [m.snare(t + k * d / 20, .12 + .25 * k / 20, (k % 2) * .2 - .1) for k in range(20)]
def horn(t, g=.32): d = .8; x = sum(osc(f * (1 + det), d, 'saw') for f in (hz('D4'), hz('F#4'), hz('A4')) for det in (-.004, .004)); m.f(lp(x, 4000) * env(int(d * SR), .01, .25), t, g, 0, .2)
def wahwah(t, g=.24):
    for i, (n, d) in enumerate([('D3', .25), ('C#3', .25), ('C3', .25), ('B2', .6)]): tt = T(d); f = hz(n) * (1 + .015 * np.sin(2 * np.pi * 6 * tt)); m.m(lp(osc(f, d, 'saw'), 900) * env(len(tt), .02, .08), t + i * .28, g, .3, .3)
def door(t, g=.8): m.thud(t, g); m.f(bp(noise(.2), 200, 1500) * dec(.2, 20), t, g * .6, .3, .3)
def roar(t, g=.45): m.crowd(t, 2.0, g); m.f(m.wav('cheer_crowd'), t + .05, g * .9, 0, .25)

m.crowd(0, S['started'], .25); m.crowd(S['oct'], S['retire'] - S['oct'], .18, swell=False); m.crowd(S['tribute'], S['twist'] - S['tribute'], .16, swell=False)
# HOOK: loud hit, sad trombone, Danish cheer
k808(0, 1.0); m.crash(0, .45); m.brass_hit([hz('D3'), hz('G#3'), hz('D4')], 0, .7, .32); m.f(m.wav('cheer_crowd'), 0, .4, .3, .2); wahwah(.5, .22); m.f(m.wav('grumble_sad'), 1.4, .35, -.2, .1)
# HOW IT STARTED
t = S['started']; m.whoosh(t, .5, .4, True); m.harp_gliss(t + .1, ['C5', 'E5', 'G5', 'C6'], .06); m.ding(t + .5, 2093, .25)
groove(S['press'], S['going'] - .1, [['C3', 'E3', 'G3'], ['A2', 'C3', 'E3'], ['F2', 'A2', 'C3'], ['G2', 'B2', 'D3']], ['E5', 'C5', 'A4', 'B4'], .8)
# press: mic tap, the bench slides in, gasp, footsteps, door
t = S['press']; m.tick(t + .3, False, .3); m.tick(t + .45, False, .3); m.whoosh(t + .5, .3, .3, False); m.thud(t + .75, .5); m.f(m.wav('ooh_crowd'), t + .8, .25, 0, .3)
m.f(m.wav('gasp'), t + 1.55, .45, .2, .1); m.brass_hit([hz('D3'), hz('G#3')], t + 1.55, .5, .25)
for k in range(10): m.footstep(t + 2.55 + k * .13, .3, .1 + k * .07)
door(t + 3.8); m.pop(t + 3.95, .3, 600)
# Oct 1: drumroll -> 4-2 WIN party, newspaper, SIUUU from the Dane
t = S['oct']; drumroll(t + .7); k808(t + 1.2, 1.0); m.crash(t + 1.2, .45); roar(t + 1.2, .5); m.firework(t + 1.4, .3, -.3); m.firework(t + 1.7, .3, .3)
m.whoosh(t + 2.0, .4, .35, True); m.f(bp(noise(.3), 2000, 7000) * env(int(.3 * SR), .01, .1), t + 2.05, .3, 0, .1); m.thud(t + 2.35, .4)
m.f(m.wav('siu'), t + 3.4, .9, .5, .25); m.f(m.wav('laugh_crowd'), t + 3.9, .3, 0, .3)
# retire: soft, hook on the wall, light off
t = S['retire']; m.music_box(t + .1, ['E5', 'D5', 'C5', 'G4', 'C5', 'E5'], .3, .14); m.tick(t + 1.3, False, .4); m.f(m.wav('chuckle'), t + 1.6, .2, 0, .1)
for k in range(6): m.footstep(t + 1.9 + k * .16, .22, -.1 - k * .1)
m.tick(t + 2.6, True, .4)
# HOW IT'S GOING
t = S['going']; m.whoosh(t, .5, .4, False); m.brass_hit([hz('D3'), hz('F3'), hz('G#3')], t + .1, .8, .3)
t = S['tribute']; m.choir([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t, 2.6, .16)
for k in range(14): m.clap(t + .2 + k * .17, .2)
m.sparkle(t + .4, 1.4, .1)
groove(S['g1'], S['consol'] - .1, [['D3', 'F3', 'A3'], ['A#2', 'D3', 'F3'], ['G2', 'A#2', 'D3'], ['A2', 'C#3', 'E3']], ['D5', 'F5', 'D5', 'C#5'], .75, 96)
GT = dict(g1=1.6, g2=1.75, g3=1.9, g4=1.7)
def siu(t, g=.9, pan=.2): m.f(m.wav('siu'), t, g, pan, .25)
def goal(t, i):
    m.net(t, .7); k808(t, 1.0); m.crash(t, .45); horn(t + .02); roar(t + .05, .45 + .05 * i); wahwah(t + .9, .2 + .03 * i)
# G1 penalty: heartbeat stare-down, run-up, kick, solo SIUUU
t = S['g1']; m.heartbeat(t + .05, .5); m.heartbeat(t + .55, .55); m.drone(hz('D2'), t, .95, .12)
m.whoosh(t + .95, .25, .4, False); [m.footstep(t + .97 + k * .08, .3) for k in range(4)]; m.thwack(t + 1.25, .9); drumroll(t + 1.15, .45); m.f(m.wav('gasp'), t + 1.3, .3, -.3, .1)
goal(t + GT['g1'], 0); siu(t + GT['g1'] + 1.25, .85)
# G2 volley: lob, slow-motion swoop, BOOM, whip pan, bigger SIUUU + shockwave
t = S['g2']; m.thwack(t + .05, .5); m.whoosh(t + .1, .6, .3, True); m.slowdown(t + .75, .7, .45); m.drone(hz('A1'), t + .75, .55, .2)
m.thud(t + 1.25, 1.0); k808(t + 1.25, 1.0); m.brass_hit([hz('D3'), hz('A3'), hz('D4')], t + 1.25, .4, .35); m.whoosh(t + 1.45, .3, .45, False)
goal(t + GT['g2'], 1); siu(t + GT['g2'] + 1.2, 1.0); m.f(lp(noise(.8), 400) * env(int(.8 * SR), .01, .5), t + GT['g2'] + 1.25, .5, 0, .2); m.f(m.wav('ooh_crowd'), t + GT['g2'] + 1.4, .3, 0, .3)
# G3 dribble: tracking footsteps, step-over spin, POV net, team SIUUU x3
t = S['g3']; [m.footstep(t + k * .09, .28, -.2 + k * .03) for k in range(14)]; m.whoosh(t + .6, .5, .4, True); m.boing(t + .65, .35, .5, 200, 500); m.tweet(t + 1.0, 3, .14, .3)
m.thwack(t + 1.3, .6); m.whoosh(t + 1.35, .5, .35, True); drumroll(t + 1.45, .45)
goal(t + GT['g3'], 2)
for d in (0, .12, .24): siu(t + GT['g3'] + 1.2 + d, .75, -.4 + d * 3)
m.firework(t + GT['g3'] + 1.5, .3, -.3); m.firework(t + GT['g3'] + 1.8, .3, .3); m.f(m.wav('grumble_angry'), t + GT['g3'] + .5, .35, -.3, .1)
# G4 header: corner kick, rising whoosh to the sky, BONK, giant SIUUUUU
t = S['g4']; m.tweet(t + .05, 1, .3, .5); m.thwack(t + .33, .7, .4); m.whoosh(t + .4, .7, .4, True); m.choir([hz('D4'), hz('A4'), hz('D5')], t + .6, .5, .12)
m.whoosh(t + 1.0, .4, .35, False); m.bonk(t + 1.38, .8); drumroll(t + 1.3, .4)
goal(t + GT['g4'], 3); m.crash(t + GT['g4'] + 1.2, .5)
for d in (0, .1, .15): siu(t + GT['g4'] + 1.2 + d, .8, -.3 + d * 4)
m.f(m.wav('siu_crowd'), t + GT['g4'] + 1.4, .6, 0, .3); m.f(m.wav('wail'), t + GT['g4'] + .8, .3, -.3, .15)
# consolation: tiny sad party
t = S['consol']; m.thwack(t + .1, .5); m.thud(t + .4, .5); m.f(m.wav('ooh_crowd'), t + .45, .25, 0, .3); m.thwack(t + .8, .35); m.net(t + 1.0, .4); m.pop(t + 1.15, .25, 900); m.f(osc(glide(700, 400, .4), .4) * env(int(.4 * SR), .01, .2), t + 1.2, .2, .2, .1)
m.f(m.wav('chuckle'), t + 1.3, .3, 0, .1); m.f(m.wav('grumble_sad'), t + 1.8, .25, 0, .1)
# twist: the stamp, then the sip
t = S['twist']; m.whoosh(t, .4, .35, True); m.brass_hit([hz('D3'), hz('A3'), hz('D4')], t + .7, .6, .32); m.thud(t + .7, .9); k808(t + .7, 1.0)
m.scratch(t + 1.85, .45); m.slurp(t + 2.1, .9, .35, .3); m.badumtss(t + 3.3, .5)
# THANKS
t = S['thanks']
for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'G5', 'E5', 'C6']): m.pluck(hz(n), t + .1 + i * .18, .6, .22, -.3 + i * .1, .5, .4)
m.saw_chord([hz('C4'), hz('E4'), hz('G4')], t + .1, 3.1, .05, 1600, 0, .3, .8, .4); m.ding(t + 1.2, 2093, .35); m.pop(t + 1.2, .3)
m.write(sys.argv[1])
