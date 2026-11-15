"""Ep12 v3 = THE 20-YEAR CHASE sound: a driving chase beat + one slapstick sound set per World Cup. No TTS.
hook 0 · 2006 2.4 · 2010 6.0 · 2014 10.2 · 2018 14.8 · 2022 18.1 · 2026 22.7 · end 27.3 · out 31.9"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
END = 31.9; m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def chase(t0, t1, g=1.0, bpm=150, root='E2'):
    b = 60 / bpm; t = t0; i = 0; f = hz(root); riff = [1, 1, 1.5, 1, 1.335, 1, 1.5, 1.78]
    while t < t1 - .02:
        if i % 2 == 0: m.kick(t, .55 * g)
        else: m.snare(t, .3 * g)
        m.hat(t + b / 2, .07 * g)
        m.bass(f * riff[i % 8], t, b * .9, .22 * g)
        t += b; i += 1
def slide(t, f0, f1, d=.5, g=.3): tt = T(d); m.f(osc(glide(f0, f1, d), d) * env(len(tt), .01, .05), t, g, 0, .15)
def trombone(t, g=.28):
    for i, (n, d) in enumerate([('D3', .25), ('C#3', .25), ('C3', .25), ('B2', .7)]): tt = T(d); m.m(lp(osc(hz(n) * (1 + .02 * np.sin(2 * np.pi * 6 * tt)), d, 'saw'), 900) * env(len(tt), .02, .08), t + i * .27, g, .2, .3)
def stampfx(t): m.thud(t, .5); m.f(bp(noise(.08), 800, 3000) * dec(.08, 40), t, .4)
def runin(t): m.whoosh(t, .5, .3, True, .3); [m.footstep(t + .1 + k * .12, .2, (-1) ** k * .3) for k in range(5)]
def vuvu(t, d):
    tt = T(d); f = 233 * (1 + .01 * np.sin(2 * np.pi * 5 * tt)); x = osc(f, d, 'saw') + .5 * osc(f * 2.01, d, 'saw'); m.f(bp(x, 200, 3000) * env(len(tt), .05, .2), t, .35, -.3, .1)
# HOOK
m.brass_hit([hz('E3'), hz('B3'), hz('E4')], 0, .7, .3); m.crash(0, .3); m.tick(.6); m.tick(.85, False)
m.f(lp(noise(.25), 3000) * dec(.25, 25) * 2, 1.15, .7); k808(1.15, 1.0); m.crash(1.15, .4)  # starter pistol
chase(1.15, 20.1, .9)
m.bonk(1.58, .8); m.f(m.wav('laugh_crowd'), 1.65, .25, 0, .3)
# 2006: glove swat, Messi flies, ball bonk on Ronaldo
t = 2.4; runin(t); m.whoosh(t + .7, .3, .3, True); m.thwack(t + 1.0, .8); m.boing(t + 1.05, .35, .6, 200, 700); slide(t + 1.1, 900, 2200, .5, .15)
m.f(m.wav('laugh_m'), t + 1.2, .3, -.4, .2); stampfx(t + 1.6)
m.whoosh(t + 2.05, .25, .3, False, .5); m.bonk(t + 2.3, .9); m.tweet(t + 2.45, 4, .15); stampfx(t + 2.6); m.f(m.wav('laugh_crowd'), t + 2.6, .3, 0, .3)
for k in range(5): m.footstep(t + 2.85 + k * .1, .2, .5)
# 2010: vuvuzela, tiki-taka passes, Spain takes it
t = 6.0; runin(t); vuvu(t + .8, 1.0)
for k in range(10): m.pop(t + 1.9 + k / 7, .25, 700 + (k % 4) * 150, (-1) ** k * .4); m.thwack(t + 1.9 + k / 7, .15, (-1) ** k * .4)
m.boing(t + 2.5, .25, .5, 300, 150); m.tweet(t + 2.7, 4, .12)
m.cheer_burst(t + 3.3, .3); m.f(m.wav('laugh_crowd'), t + 3.4, .25, 0, .3)
for k in range(8): m.footstep(t + 3.3 + k * .08, .15, .4)
# 2014: barrier clang, poof to VIP, glass clonk, sad trombone, golden ball, walk past
t = 10.2; runin(t); m.whoosh(t + .75, .2, .25, False); x = sum(a * osc(f, .6) for f, a in [(310, 1), (777, .6), (1450, .4)]) * dec(.6, 7); m.f(x, t + 1.0, .5); m.pop(t + 1.45, .4, 500); m.sparkle(t + 1.5, .5, .1)
m.whoosh(t + 2.0, .25, .3, False); m.ding(t + 2.06, 2637, .35); m.f(hp(noise(.2), 3000) * dec(.2, 20), t + 2.06, .3)
trombone(t + 2.3); m.sparkle(t + 2.9, .6, .15); m.ding(t + 2.95, 1760, .25)
m.music_box(t + 3.4, ['E5', 'D5', 'C5', 'B4', 'A4'], .25, .1)
# 2018: holes, slide-whistle drop, pop-up boing, calendar
t = 14.8; runin(t); m.pop(t + 1.35, .4, 400); slide(t + 1.5, 1600, 300, .45, .3); m.thud(t + 1.9, .5)
m.boing(t + 2.1, .3, .4, 200, 500); m.tweet(t + 2.2, 4, .12); m.f(bp(noise(.15), 1000, 4000) * dec(.15, 15), t + 1.9, .3); m.f(m.wav('laugh_crowd'), t + 1.7, .3, 0, .3)
for k in range(5): m.footstep(t + 2.5 + k * .1, .2, .5)
# 2022: bench slides in, trophy runs past, dive, CATCH, bisht, fireworks
t = 18.1; runin(t); m.whoosh(t + .75, .3, .3, True, -.5); m.thud(t + 1.0, .5); stampfx(t + 1.05)
for k in range(7): m.footstep(t + 1.2 + k * .11, .2, .5 - k * .15)
m.whoosh(t + 1.6, .4, .35, True); m.heartbeat(t + 1.5, .3)
c = t + 2.0; m.brass_hit([hz('E3'), hz('B3'), hz('E4'), hz('G#4'), hz('B4')], c, 1.2, .45); m.crash(c, .5); m.cheer_burst(c, .4); m.whoosh(c + .25, .4, .25, False)
m.choir([hz('E4'), hz('G#4'), hz('B4'), hz('E5')], c + .2, 2.4, .12)
for i in range(5): m.firework(c + .3 + i * .45, .3, -.5 + i * .25)
m.harp_gliss(c + .4, ['E5', 'F#5', 'G#5', 'B5', 'C#6', 'E6'], .05, .12); m.f(m.wav('gasp'), c + .3, .3, .4, .2)
# 2026: last chance, penalty, SIUUU, Spain stampede
t = 22.7; runin(t); chase(t + .3, t + 2.6, .7, 160, 'F2'); m.heartbeat(t + .7, .35)
m.thwack(t + 1.15, .8); m.net(t + 1.4, .6); m.cheer_burst(t + 1.45, .4); m.f(m.wav('siu'), t + 1.55, .9, 0, .25); m.f(m.wav('siu_crowd'), t + 1.75, .5, 0, .3)
for k in range(22): m.footstep(t + 2.6 + k * .045, .3, .5 - k * .045)
m.bonk(t + 2.75, .7); m.f(lp(noise(.3), 400) * dec(.3, 10), t + 2.75, .5); m.f(m.wav('laugh_crowd'), t + 3.0, .35, 0, .3); trombone(t + 3.2, .22)
# END: sunset, bubbles, mate slurp, question
t = 27.3; runin(t)
for i, n in enumerate(['E4', 'G#4', 'B4', 'E5', 'D#5', 'B4', 'G#4', 'E4', 'F#4', 'A4', 'C#5', 'E5']): m.pluck(hz(n), t + .5 + i * .3, .7, .14, -.3 + .05 * i, .4, .4)
m.pop(t + 1.3, .3); m.slurp(t + 2.0, .7, .3); m.ding(t + 2.5, 1318, .3); m.pop(t + 2.8, .3, 900); m.pop(t + 2.95, .3, 1100); m.f(m.wav('ooh_crowd'), t + 2.6, .3, 0, .3)
m.write(sys.argv[1])
