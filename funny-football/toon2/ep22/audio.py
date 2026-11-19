"""Ep22 SO CLOSE sound: lounge-jazz gala (walking bass + brushed snare + vibes, new style) / stadium for the Clásico / swagger funk for the moonwalk.
gala1 0 · rewind 2.5 · clasico1 3.2 · clasico2 6.5 · moon 9.0 · reveal 11.0 · smile 15.0 · flash 19.0 · end 24.0 · END 28.0"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 28.0; m = Mix2(END, ep=22)
def jazz(t0, t1, g=.6, bpm=120):
    b = 60 / bpm; t = t0; i = 0; walk = ['C2', 'E2', 'G2', 'A2', 'D2', 'F2', 'A2', 'B2', 'G2', 'B2', 'D3', 'E3', 'C2', 'E2', 'G2', 'G#2']; vib = ['E5', 'G5', 'B5', 'D6']
    while t < t1 - .02:
        m.bass(hz(walk[i % 16]), t, b * .9, .28 * g); m.f(bp(noise(.12), 2000, 7000) * env(int(.12 * SR), .03, .08), t + b / 2, .05 * g)
        if i % 4 == 0: m.xylo(t, [vib[(i // 4) % 4]], .05, .12 * g)
        t += b; i += 1
def whistle(t, n=1, g=.3):
    for k in range(n): d = .22 if n > 1 else .4; tt = T(d); m.f(osc(2800 * (1 + .03 * np.sin(2 * np.pi * 40 * tt)), d) * env(len(tt), .01, .03), t + k * .3, g, 0, .2)
def roar(t, g=.45, d=1.6): m.crowd(t, 'cheer', d, g)
# GALA 1
jazz(0, 2.5, .8); m.crowd(.1, 'cheer', .8, .12); m.vo('mbappe', 'laugh', .6, .4, -.3, 'snicker'); m.timpani(1.0, 90, .3, roll=1.3)
# REWIND
m.tape_rewind(2.5, .7, .45)
# CLÁSICO 1: lucky pinball + equaliser
t = 3.2; m.f(bp(noise(3.3), 300, 1800) * .25, t, .3); whistle(t + .05); m.thwack(t + .05, .6)
m.boing(t + .4, .4, .4, 200, 400); m.f(osc(2600, .5) * dec(.5, 6), t + .8, .25); m.bonk(t + 1.2, .6); m.vo('mbappe', 'oof', t + 1.22, .5); m.thump(t + 1.6, .5); roar(t + 1.62, .45); m.vo('mbappe', 'yay', t + 1.8, .5)
m.thump(t + 2.4, .4); m.crowd(t + 2.45, 'cheer', 1.0, .3, .4)
# CLÁSICO 2: the sprint + winner + 100
t = 6.5; m.f(bp(noise(2.5), 300, 1800) * .25, t, .3); m.whoosh(t, 1.0, .4, True, .3)
for i in range(3): m.smack(t + .3 + i * .22, .4, (-1) ** i * .3)
m.thwack(t + .95, .8); m.boom(t + 1.0, .45); roar(t + 1.02, .6, 2.0); m.vo('mbappe', 'siu', t + 1.2, .6); m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t + 1.4, .9, .25); whistle(t + 2.2, 3, .3)
# MOON: swagger funk
t = 9.0; m.oompah(t, t + 2.0, ('E2', 'B1'), 150, .5); m.kazoo(t + .2, ['E4', 'G4', 'A4', 'B4', 'A4', 'G4'], .25, .1); m.sparkle(t + .3, 1.2, .15); m.vo('mbappe', 'laugh', t + 1.0, .45, 0, 'cackle')
# REVEAL
t = 11.0; jazz(t, t + 1.0, .5); m.timpani(t + .1, 85, .45, roll=.7); m.brass_hit([hz('D4'), hz('F#4'), hz('A4')], t + .9, .8, .25); m.crowd(t + .95, 'cheer', 1.6, .35, .4)
m.whoosh(t + 1.3, .5, .35, True, .3); m.scratch(t + 1.5, .5); m.vo('mbappe', 'gasp', t + 1.55, .6); m.zip(t + 2.2, .35); m.f(osc(glide(400, 900, .8), .8, 'tri') * env(int(.8 * SR), .01, .1), t + 2.2, .12); m.cork(t + 3.0, .3)
# SMILE: stiff claps, eye twitch squeaks, glass crack
t = 15.0
for i in range(8): m.f(hp(noise(.04), 1500) * dec(.04, 60), t + .25 + i * .5, .5)
for i in range(6): m.squeak(t + 1.0 + i * .15, .15)
m.f(hp(noise(.5), 3000) * dec(.5, 6) + .3 * osc(glide(3000, 1500, .5), .5) * dec(.5, 8), t + 2.6, .45); m.vo('mbappe', 'whistle' if False else 'hmm', t + 3.0, .4)
# FLASH: three stingers, sad kazoo
t = 19.0
for i in range(3): m.boom(t + i * 1.65, .3); m.wahwah(t + i * 1.65 + .1, .12) if i == 2 else m.timpani(t + i * 1.65, 70 - i * 6, .4)
m.vo('mbappe', 'cry', t + 1.8, .5, 0, 'whimper', 1.3); m.vo('mbappe', 'cry', t + 3.5, .55, 0, 'sob', 1.4)
# END: rain + sad jazz + pat pat
t = 24.0; m.rain(t, 4.0, .1); jazz(t, END, .4, 84); m.f(hp(noise(.05), 1200) * dec(.05, 40), t + 1.65, .4); m.f(hp(noise(.05), 1200) * dec(.05, 40), t + 1.85, .4); m.vo('kane', 'laugh', t + 1.9, .4, .3, 'snicker'); m.vo('mbappe', 'cry', t + 2.2, .55, -.2, 'blubber', 1.4)
m.write(sys.argv[1])
