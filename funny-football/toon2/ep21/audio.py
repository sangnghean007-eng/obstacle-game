"""Ep21 MBAPPÉ THIS SEASON sound: bright ukulele-style strum (happy) that dies on a phone buzz → tremolo strings + muted-trumpet fail. vox2/fx2 only.
m1 0 · m2 1.8 · m3 4.5 · m4 6.1 · m5 8.7 · END 12.1"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 12.1; m = Mix2(END, ep=21)
def uke(t0, t1, g=.6, bpm=132):
    b = 60 / bpm; t = t0; i = 0; ch = [['C4', 'E4', 'G4', 'C5'], ['A3', 'C4', 'E4', 'A4'], ['F3', 'A3', 'C4', 'F4'], ['G3', 'B3', 'D4', 'G4']]
    while t < t1 - .02:
        for k, n in enumerate(ch[(i // 4) % 4][::(1 if i % 2 == 0 else -1)]): m.pluck(hz(n), t + k * .012, .25, .09 * g, .2, 1.8)
        if i % 2 == 0: m.kick(t, .2 * g)
        else: m.clap(t, .08 * g)
        t += b / 2; i += 1
def strings(t0, d, g=.12):
    for n in ('A3', 'C4', 'E4'): tt = T(d); x = osc(hz(n) * (1 + .006 * np.sin(2 * np.pi * 5.5 * tt)), d, 'saw') * (0.6 + 0.4 * np.sin(2 * np.pi * 12 * tt)); m.m(lp(x, 2200) * env(len(tt), .3, .6), t0, g, 0, .4)
uke(0, 4.6, .8)
for k, t in enumerate([0.9, 2.16, 3.06, 3.96]): m.thwack(t - .5, .5); m.thump(t, .5); m.crowd(t + .02, 'cheer', 1.0, .25 + k * .05); m.vo('mbappe', ['yay', 'laugh', 'yay', 'laugh'][k], t + .1, .5, 0, *(['belly', 1.0] if k % 2 else []))
m.slide_whistle(4.3, True, .4, .15)
# the buzz: music cut, vibration, gulp
m.scratch(4.88, .5); m.f(osc(150, .6, 'sq') * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 18 * T(.6)))) * .4, 4.9, .35); m.f(osc(150, .6, 'sq') * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 18 * T(.6)))) * .4, 5.6, .3)
m.vo('mbappe', 'uhoh', 5.9, .6)
# collapse: tremolo strings, trembling squeaks, sob
strings(6.1, 2.8, .1); [m.squeak(6.4 + i * .3, .15) for i in range(6)]; m.vo('mbappe', 'cry', 7.4, .55, 0, 'whimper', 1.3)
# end card
m.wahwah(8.8, .22); m.vo('mbappe', 'cry', 9.2, .6, 0, 'blubber', 1.6); m.crowd(9.6, 'laugh', 1.6, .2)
m.write(sys.argv[1])
