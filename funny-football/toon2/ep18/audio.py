"""Ep18 THE MIRACLE sound: stadium drums + brass (big-final feel, new for the series), crowd swells, goal roars, dressing-room drip + rising hum,
power-up whoosh, rocket header, pinball bonks, noodle-legs boing, moon whistle. vox2/fx2 only.
hook 0 · crespo 3.2 · selfie 7.2 · song 10.5 · six 14.1 · save 22.7 · pens 26.1 · end 33.7 · END 38.7"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
END = 38.7; m = Mix2(END, ep=18)
def drums(t0, t1, g=.6, bpm=100):
    b = 60 / bpm; t = t0; i = 0
    while t < t1 - .02: (m.timpani(t, 70 if i % 4 == 0 else 98, .25 * g) if i % 2 == 0 else m.clap(t, .12 * g)); t += b / 2; i += 1
def anthem(t0, t1, g=.18):  # original brass fanfare line (not any real anthem)
    mel = ['C4', 'E4', 'G4', 'C5', 'B4', 'G4', 'A4', 'F4', 'G4', None]; st = .3; t = t0; i = 0
    while t < t1 - .02:
        n = mel[i % len(mel)]
        if n: m.brass_hit([hz(n), hz(n) * 1.5], t, st * .9, g)
        t += st; i += 1
def whistle(t, n=1, g=.3):
    for k in range(n): d = .25 if n > 1 else .45; tt = T(d); m.f(osc(2800 * (1 + .03 * np.sin(2 * np.pi * 40 * tt)), d) * env(len(tt), .01, .03), t + k * .32, g, 0, .2)
def roar(t, g=.45, d=2.0): m.crowd(t, 'cheer', d, g); m.f(bp(noise(d), 200, 2500) * env(int(d * SR), .05, 1.0), t, g * .6, 0, .3)
m.f(bp(noise(END), 300, 1800) * .2, 0, .22, 0, .1)
# HOOK: kick-off, yawn, thunder volley
whistle(.05); m.vo('generic_m', 'hmm', .2, .4, -.3); m.whoosh(.9, .5, .3, True, .3); m.thwack(.9, .8); m.thump(1.4, .7); roar(1.45, .35, 1.4); m.vo('maldini' if False else 'generic_m', 'laugh', 1.6, .5, .4, 'point'); drums(0, 3.2, .5)
# CRESPO: pinball bonks, faceplant
t = 3.2
for i in range(3): m.smack(t + .4 + i * .35, .7, (-1) ** i * .3); m.xylo(t + .42 + i * .35, [['G5', 'C6', 'E6'][i]], .05, .2); m.vo(['generic_m', 'big', 'generic_m'][i], 'oof', t + .42 + i * .35, .5)
m.thump(t + 1.5, .6); roar(t + 1.5, .3, 1.2); m.slide_whistle(t + 2.6, True, .4, .2); m.thump(t + 2.95, .8); m.vo('generic_m', 'ow', t + 3.0, .6); roar(t + 3.3, .3, 1.0); m.vo('generic_m', 'laugh', t + 1.7, .5, .4, 'cackle')
# SELFIE: shutter clicks, smug giggles, red end sobs
t = 7.2; whistle(t, 2)
for k in range(4): m.f(bp(noise(.03), 2000, 6000) * dec(.03, 90), t + .7 + k * .33, .5)
m.vo('generic_m', 'laugh', t + .5, .5, .3, 'snicker'); m.vo('generic_f', 'laugh', t + 1.0, .4, .4, 'giggle'); m.vo('kid', 'cry', t + .6, .3, -.4, 'whimper', 1.6); m.wahwah(t + 1.6, .15)
# SONG: drip, sobs, then the hum swells through the door → power-up
t = 10.5
for k in range(6): m.f(osc(glide(1200, 600, .08), .08) * dec(.08, 30), t + k * .3, .2, .3)
m.vo('generic_m', 'cry', t + .1, .45, -.3, 'sob', 1.6)
for i in range(10): m.vo(['generic_m', 'big', 'generic_f', 'generic_m'][i % 4], 'hmm', t + .6 + i * .12, .18 + i * .02, .6 - i * .1)
m.timpani(t + 1.2, 75, .4, roll=.8); m.whoosh(t + 2.0, .8, .45, True, 0); m.f(osc(glide(80, 400, 1.0), 1.0, 'saw') * env(int(SR), .1, .3), t + 2.0, .15); m.vo('generic_m', 'yay', t + 2.2, .5)
# SIX MINUTES: drums + brass, rocket, zigzag, rebound
t = 14.1; drums(t, t + 8.6, .8, 120); anthem(t + .2, t + 8.4, .1)
m.f(lp(noise(.8), 2500) * env(int(.8 * SR), .1, .1), t + .6, .4); m.boom(t + 1.4, .6); roar(t + 1.45, .55, 2.0)
for k in range(5): m.squeak(t + 3.2 + k * .14, .25)
m.thump(t + 3.9, .6); roar(t + 3.95, .55, 2.0); m.vo('generic_m', 'uhoh', t + 3.4, .5, .4)
m.thwack(t + 5.6, .7); m.smack(t + 6.1, .8, .3); m.vo('generic_m', 'oof', t + 6.12, .6, .3); m.thwack(t + 6.6, .9); m.boom(t + 6.9, .6); roar(t + 6.95, .6, 2.4); m.crowd(t + 7.3, 'gasp', 1.0, .3, .5)
# SAVE: heartbeat, face save, hand save
t = 22.7; m.heartbeat(t, .4); m.heartbeat(t + .5, .4); m.thwack(t + .5, .7); m.smack(t + .72, .8, -.3); m.vo('generic_m', 'oof', t + .74, .6, -.3); m.thwack(t + 1.3, .7); m.smack(t + 1.52, .6, -.3); m.whoosh(t + 1.55, .5, .3, True); m.crowd(t + 1.6, 'gasp', 1.2, .4); m.vo('generic_m', 'no', t + 1.8, .4, .3)
# PENS: noodle boings, hypnosis, moon
t = 26.1; whistle(t)
for k in range(14): m.spring(t + k * .52, .12, .4)
for a, how in ((0.0, 'over'), (2.2, 'saved'), (4.4, 'saved')):
    m.heartbeat(t + a + .2, .35); m.f(osc(glide(400, 900, .8) * (1 + .05 * np.sin(2 * np.pi * 8 * T(.8))), .8, 'tri') * env(int(.8 * SR), .1, .2), t + a + .1, .12); m.thwack(t + a + 1.15, .7)
    if how == 'over': m.slide_whistle(t + a + 1.2, True, .8, .3); m.vo('generic_m', 'uhoh', t + a + 1.7, .5, .3)
    else: m.smack(t + a + 1.55, .7, -.3); m.crowd(t + a + 1.6, 'cheer', 1.0, .35)
m.vo('generic_m', 'grunt', t + 5.8, .5, .3); m.thump(t + 6.1, .5); m.vo('generic_m', 'laugh', t + 6.4, .5, -.3, 'belly', 1.0)
# END: the roar, trophy, sobbing loser
t = 33.7; roar(t, .7, 4.0); m.firework(t + .3, .3); m.firework(t + 1.0, .3, .4); m.brass_hit([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t + .1, 1.4, .25); anthem(t + 1.4, END - .3, .12)
m.vo('generic_m', 'cry', t + .8, .35, .5, 'blubber', 1.2); for_ = [m.spring(t + 2.0 + k * .5, .1, .4) for k in range(5)]
m.write(sys.argv[1])
