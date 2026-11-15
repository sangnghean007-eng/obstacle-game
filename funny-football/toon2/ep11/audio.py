"""Ep11 TWO LIVES sound: one evolving music bed (2002 → 2026), a tick per year, a chime per milestone, fanfares for 2016/2022, crowd on BOTH years. No TTS."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
Y = json.loads(sys.argv[2]); EV = json.loads(sys.argv[3]); END = float(sys.argv[4]); TL_END = float(sys.argv[5])
m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
# hook
k808(0, 1.0); m.crash(0, .4); m.brass_hit([hz('D3'), hz('A3'), hz('D4')], 0, .8, .32); m.f(m.wav('cheer_crowd'), 0, .3, 0, .2)
# music bed: tempo rises over the years
t = 2.4; i = 0; prog = [['D3', 'F#3', 'A3'], ['B2', 'D3', 'F#3'], ['G2', 'B2', 'D3'], ['A2', 'C#3', 'E3']]
while t < TL_END - .05:
    bpm = 96 + (t - 2.4) / (TL_END - 2.4) * 40; b = 60 / bpm
    m.saw_chord([hz(n) for n in prog[i % 4]], t, 4 * b * .95, .05, 1500, 0, .2, .3, .4)
    for k in (0, 1.5, 2.5): k808(t + k * b, .55)
    for k in (1, 3): m.clap(t + k * b, .26)
    for k in range(8): m.hat(t + k * b / 2, .06)
    t += 4 * b; i += 1
for y, ys, yd in Y:
    m.tick(ys, True, .25); m.pop(ys + .02, .15, 1400)
    evs = [e for e in EV if e[0] == y]
    for j, e in enumerate(evs):
        tt = ys + .15 + j * .12; pan = -.5 if e[1] == 'R' else .5
        if e[3] in ('bdo', 'ucl', 'cup', 'wc'): m.ding(tt, 1568 if e[3] == 'bdo' else 1318, .2, pan)
        elif e[3] == 'move': m.whoosh(tt, .4, .3, True, pan)
        elif e[3] == 'goal': m.sparkle(tt, .6, .12)
        elif e[3] == 'bye': m.music_box(tt, ['E5', 'D5', 'C5'], .15, .12)
    if y in (2016, 2022): m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4')], ys + .2, .9, .32); m.cheer_burst(ys + .25, .4); m.firework(ys + .5, .3, -.5 if y == 2016 else .5)
    if y in (2008, 2009, 2021, 2023, 2026): m.f(m.wav('ooh_crowd' if y != 2008 else 'cheer_crowd'), ys + .4, .3, 0, .3)
# end + thanks
t = TL_END; m.whoosh(t, .6, .4, True); m.brass_hit([hz('D3'), hz('A3'), hz('D4')], t + .6, .8, .3); m.f(m.wav('bleat'), t + 1.0, .3, 0, .1); m.ding(t + 1.8, 2093, .3)
t = END - 2.8
for i, n in enumerate(['D5', 'F#5', 'A5', 'D6', 'A5', 'F#5', 'D6']): m.pluck(hz(n), t + .1 + i * .16, .6, .22, -.3 + i * .1, .5, .4)
m.ding(t + 1.0, 2093, .35); m.pop(t + 1.0, .3)
m.write(sys.argv[1])
