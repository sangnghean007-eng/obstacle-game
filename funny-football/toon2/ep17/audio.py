"""Ep17 THE GRASS IS GREENER sound: French accordion-ish waltz (Paris) vs Spanish guitar strum (Madrid), jump fails, cannon BOOM, pretzel lasso, door SLAM, rain. No TTS.
hook 0 · tantrum 3 · madrid 6.5 · split25 9.5 · split26 15 · back 20.5 · end 26.5 · END 31"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 31.0; m = Mix2(END, ep=17)
def waltz(t0, t1, g=.6, bpm=150, key='C'):
    b = 60 / bpm; t = t0; i = 0; mel = ['E4', 'G4', 'C5', 'B4', 'G4', 'E4', 'F4', 'A4', 'D5', 'C5', 'A4', 'F4']; bass = ['C3', 'G2', 'F2', 'G2']
    while t < t1 - .02:
        if i % 3 == 0: m.bass(hz(bass[(i // 6) % 4]), t, b * .9, .25 * g)
        else: m.organ_stab([hz('E4'), hz('G4')], t, .12, .05 * g)
        m.pluck(hz(mel[i % 12]), t, b * .9, .16 * g, .2); t += b; i += 1
def flamenco(t0, t1, g=.6, bpm=120):
    b = 60 / bpm; t = t0; i = 0; ch = [['E3', 'G#3', 'B3'], ['F3', 'A3', 'C4'], ['G3', 'B3', 'D4'], ['F3', 'A3', 'C4']]
    while t < t1 - .02:
        for k, n in enumerate(ch[(i // 2) % 4]): m.pluck(hz(n), t + k * .02, .4, .14 * g, -.2)
        if i % 2: m.clap(t, .2 * g)
        t += b / 2; i += 1
def creak(t, d=.6, g=.25): cr = bp(osc(glide(220, 520, d, .5), d, 'saw'), 300, 2500) * (1 + .6 * np.sin(2 * np.pi * 23 * T(d))) * env(int(d * SR), .02, .1); m.f(cr, t, g, .2, .2)
def sad_trombone(t, g=.25):
    for i, n in enumerate(['D4', 'C#4', 'C4', 'B3']): d = .4 if i < 3 else 1.0; tt = T(d); m.m(osc(hz(n) * (1 + .01 * np.sin(2 * np.pi * 5 * tt)), d, 'saw') * env(len(tt), .02, .1), t + i * .4, g, 0, .3)
# HOOK: 7 jumps, 7 misses
waltz(0, 6.5, .7)
for i in range(7): t = i * .42; m.spring(t + .02, .2, .3); m.slide_whistle(t + .15, False, .25, .12, (-1) ** i * .3); m.thump(t + .3, .35); m.vo('mbappe', ['grunt', 'oof', 'yelp'][i % 3], t + .05, .5)
m.vo('mbappe', 'hmph', 2.75, .7)
# TANTRUM
t = 3.0
for i in range(5): m.thud(t + i * .3, .4); m.f(lp(noise(.1), 600) * dec(.1, 30), t + i * .3, .3)
m.vo('mbappe', 'grunt', t + .2, .6); m.vo('mbappe', 'hmph', t + .9, .6); m.zip(t + 1.4, .35); m.thump(t + 1.45, .4); m.cork(t + 1.6, .3); m.crowd(t + 2.0, 'gasp', 1.0, .2, -.4)
for i in range(8): m.footstep(t + 2.4 + i * .13, .25, .3)
# MADRID
t = 6.5; flamenco(t, 9.5, .8); m.brass_hit([hz('E4'), hz('G#4'), hz('B4')], t + 1.0, .6, .2); m.sparkle(t + 1.1, .8, .15); m.crowd(t + .8, 'cheer', 1.6, .25); m.vo('mbappe', 'yay', t + 1.6, .5)
# SPLIT 2025
t = 9.5; m.crowd(t + .6, 'cheer', 2.0, .3, -.3); m.crash(t + .6, .25); m.choir([hz('C4'), hz('E4'), hz('G4')], t + .6, 1.4, .1)
for i in range(4): m.thud(t + 1.2 + i * .15, .25, .3)
m.vo('mbappe', 'uhoh', t + 1.7, .7); m.boom(t + 2.6, .9); m.vo('mbappe', 'yelp', t + 2.7, .7); m.vo('mbappe', 'cry', t + 3.3, .6, 0, 'wail', 1.4); m.wahwah(t + 3.4, .2)
# SPLIT 2026
t = 15.0; m.crowd(t + .5, 'cheer', 2.0, .3, -.3); m.choir([hz('D4'), hz('F#4'), hz('A4')], t + .5, 1.2, .1); m.ding(t + .55, 1568, .2)
for i in range(6): m.footstep(t + 1.0 + i * .1, .25, .3)
m.whip(t + 2.0, .45, .2); m.spring(t + 2.5, .4, .5); m.vo('kane', 'laugh', t + 2.6, .7, .3, 'cackle'); m.vo('mbappe', 'gasp', t + 2.5, .6); creak(t + 2.6, .5, .25); m.slide_whistle(t + 3.2, False, .6, .3, -.2); m.thump(t + 3.8, .7); m.vo('mbappe', 'cry', t + 3.9, .6, 0, 'blubber', 1.0)
# BACK
t = 20.5; waltz(t, t + 2.4, .5)
for i in range(8): m.footstep(t + i * .15, .2, .3)
m.vo('mbappe', 'whimper' if False else 'hmm', t + .9, .5); creak(t + 1.4, .4, .3); m.xylo_rise(t + 1.6, .15); m.vo('generic_m', 'laugh', t + 2.0, .6, 0, 'snicker', .5)
m.thump(t + 2.4, 1.0); m.smack(t + 2.41, .9); m.clang(t + 2.45, .3); m.vo('mbappe', 'oof', t + 2.42, .8); m.vo('mbappe', 'cry', t + 2.9, .6, 0, 'sob', 1.4); m.cork(t + 3.2, .35); m.crowd(t + 2.7, 'laugh', 2.2, .35, .3)
# END: rain + sad waltz + party behind the window
t = 26.5; m.rain(t, 4.5, .12); waltz(t, END, .45, 120); m.vo('mbappe', 'cry', t + .3, .6, -.3, 'whimper', 2.0); m.crowd(t + .6, 'laugh', 2.0, .25, .4); m.kazoo(t + 3.6, ['G4', 'F#4', 'F4', 'E4'], .2, .15)
m.write(sys.argv[1])
