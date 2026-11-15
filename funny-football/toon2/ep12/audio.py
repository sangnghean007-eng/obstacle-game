"""Ep12 = WORLD CUPS sound: samba groove, trophy dings, drumroll, sad trombone for the bag, record-scratch BUT…, SIUUU twist. No TTS."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
END = 22.7; m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def samba(t0, t1, g=1.0, bpm=104):
    b = 60 / bpm; t = t0; i = 0; prog = [['D3', 'F#3', 'A3'], ['G2', 'B2', 'D3'], ['A2', 'C#3', 'E3'], ['D3', 'F#3', 'A3']]
    while t < t1 - .05:
        m.saw_chord([hz(n) for n in prog[i % 4]], t, 4 * b * .95, .045 * g, 1600, 0, .2, .3, .4)
        for k in range(16): m.hat(t + k * b / 4, .05 * g if k % 4 else .09 * g)
        for k in (0, 1.5, 2.5): k808(t + k * b, .55 * g)
        for k in (0.75, 1.75, 2.75, 3.5): m.rim(t + k * b, .22 * g)
        m.pluck(hz(['A5', 'F#5', 'E5', 'D5'][i % 4]), t + 3 * b, .25, .1 * g, .3, .9, .3)
        t += 4 * b; i += 1
k808(0, 1.0); m.crash(0, .4); m.brass_hit([hz('D3'), hz('A3'), hz('D4')], 0, .8, .32)
samba(.2, 8.9, .9)
for start, cups in [(1.6, 3), (4.2, 2), (6.6, 1)]:
    m.whoosh(start, .3, .3, True, -.4)
    for c in range(cups): m.ding(start + .5 + c * .35 + .2, 1568 + c * 200, .28, .3); m.thud(start + .5 + c * .35 + .2, .3)
    m.cheer_burst(start + .6 + cups * .35, .25)
# CR7 row: drumroll, bag drop, sad trombone, laugh
t = 8.8; m.whoosh(t, .3, .3, True, -.4); [m.snare(t + .5 + k * .05, .1 + .25 * k / 22) for k in range(22)]
m.thud(t + 1.6, .9); m.f(bp(noise(.4), 200, 1200) * env(int(.4 * SR), .01, .2), t + 1.6, .4)
for i, (n, d) in enumerate([('D3', .3), ('C#3', .3), ('C3', .3), ('B2', .8)]): tt = T(d); f = hz(n) * (1 + .02 * np.sin(2 * np.pi * 6 * tt)); m.m(lp(osc(f, d, 'saw'), 900) * env(len(tt), .02, .08), t + 1.9 + i * .33, .3, .2, .3)
m.f(m.wav('laugh_crowd'), t + 2.1, .3, 0, .3)
# BUT…: record scratch + silence + shaking bag
t = 11.9; m.scratch(t, .55); m.f(bp(noise(.6), 300, 2000) * dec(.6, 6), t + .3, .25, .3)
# twist: rip + loot pops + SIUUU
t = 12.7; m.f(bp(noise(.3), 1500, 6000) * env(int(.3 * SR), .005, .2), t, .6, .2); k808(t, 1.0); m.crash(t, .5); m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4')], t + .1, .9, .35)
samba(t + .1, 17.6, 1.0, 120)
for j in range(6): m.pop(t + .25 + j * .55, .3, 900 + j * 120); m.ding(t + .3 + j * .55, 1800 + j * 150, .2, -.3 + j * .12)
m.f(m.wav('siu'), t + 3.9, 1.0, 0, .25); m.f(m.wav('siu_crowd'), t + 4.1, .6, 0, .3); m.firework(t + 4.0, .35, -.3); m.firework(t + 4.3, .35, .3)
# question + thanks
t = 17.6; m.ding(t, 1318, .3); m.pop(t + .3, .3); m.pop(t + .45, .3); m.f(m.wav('ooh_crowd'), t + .2, .3, 0, .3)
t = 20.1
for i, n in enumerate(['D5', 'F#5', 'A5', 'D6', 'A5', 'F#5', 'D6']): m.pluck(hz(n), t + .1 + i * .16, .6, .22, -.3 + i * .1, .5, .4)
m.ding(t + 1.0, 2093, .35); m.pop(t + 1.0, .3)
m.write(sys.argv[1])
