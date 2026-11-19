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
END = 12.2; m = Mix2(END, ep=2101)
uke(0, 6.0, .85, 140)
for k, t in enumerate([0.6, 1.5, 4.0 - 1.1, 4.0 + .1]): pass
# goal 1 (0.6), goal 2 knee slide (1.5–2.9), goal 3 overhead (2.9–4.5), king (4.5–6.0)
m.thwack(.1, .5); m.thump(.6, .5); m.crowd(.62, 'cheer', .9, .3); m.vo('mbappe', 'yay', .7, .5)
m.f(lp(noise(1.2), 900) * env(int(1.2 * SR), .05, .3), 1.55, .35); m.crowd(1.5, 'cheer', 1.2, .35); m.vo('mbappe', 'laugh', 1.7, .5, 0, 'belly', 1.0)
m.whoosh(3.2, .4, .3); m.f(hp(noise(.3), 3000) * dec(.3, 8), 3.38, .4); m.thwack(3.4, .8); m.thump(4.0, .6); m.crowd(4.02, 'cheer', 1.4, .45); m.vo('mbappe', 'siu', 4.1, .5)
m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], 4.5, 1.2, .25); m.sparkle(4.5, 1.0, .2); m.crowd(4.6, 'cheer', 1.4, .3); m.vo('mbappe', 'laugh', 5.0, .5, 0, 'cackle')
# buzz (6.0): music cut, vibration; PSG burst out (6.9), conga, trophy BONK (8.45)
m.scratch(5.98, .5); vib = osc(150, .6, 'sq') * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 18 * T(.6)))) * .4; m.f(vib, 6.0, .35); m.vo('mbappe', 'uhoh', 6.6, .6)
m.f(hp(noise(.4), 1500) * dec(.4, 8), 6.9, .5)
for i in range(4): m.slide_whistle(6.9 + i * .18, False, .4, .15, (-1) ** i * .4); m.vo(['generic_m', 'kid', 'big', 'generic_f'][i], 'yay', 7.2 + i * .15, .35, -.5 + i * .33)
m.kazoo(7.4, ['C5', 'E5', 'G5', 'E5', 'C5', 'E5', 'G5', 'C6'], .18, .12); m.crowd(7.6, 'laugh', 1.6, .35); m.clang(8.45, .5); m.vo('mbappe', 'oof', 8.47, .6)
# collapse + end (9.2)
strings(9.2, 3.0, .1); m.rain(9.2, 3.0, .1); m.wahwah(9.3, .2); m.vo('mbappe', 'cry', 9.5, .6, 0, 'blubber', 1.8)
m.write(sys.argv[1])
