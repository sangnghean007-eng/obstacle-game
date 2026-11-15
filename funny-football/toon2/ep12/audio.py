"""Ep12 v2 = THE WORLD CUP'S EXES sound: each era its own sound world. No TTS.
hook 0 · pele 2.2 · r94 8.2 · r02 11.2 · messi 14.8 · cr7 18.8 · question 25.8 · thanks 28.4 · end 30.8"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
END = 30.8; m = Mix(END)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def samba(t0, t1, g=1.0, bpm=110):
    b = 60 / bpm; t = t0; i = 0; prog = [['D3', 'F#3', 'A3'], ['G2', 'B2', 'D3'], ['A2', 'C#3', 'E3'], ['D3', 'F#3', 'A3']]
    while t < t1 - .05:
        m.saw_chord([hz(n) for n in prog[i % 4]], t, min(4 * b * .95, t1 - t), .045 * g, 1600, 0, .2, .3, .4)
        for k in range(16):
            if t + k * b / 4 < t1: m.hat(t + k * b / 4, .05 * g if k % 4 else .09 * g)
        for k in (0, 1.5, 2.5):
            if t + k * b < t1: k808(t + k * b, .55 * g)
        for k in (0.75, 1.75, 2.75, 3.5):
            if t + k * b < t1: m.rim(t + k * b, .22 * g)
        t += 4 * b; i += 1
def crackle(t0, t1, g=.12):  # old film projector: hiss + random pops + 24fps flutter
    d = t1 - t0; x = hp(noise(d), 3000) * .15; n = len(x); idx = np.random.default_rng(3).integers(0, n, int(d * 18)); x[idx] += np.random.default_rng(4).standard_normal(len(idx)) * 3
    x *= (1 + .3 * np.sin(2 * np.pi * 24 * T(d))); m.f(x, t0, g, 0, .05)
def romance(t, notes, step=.32, g=.16):  # soft rhodes-ish love theme
    for i, n in enumerate(notes): m.pluck(hz(n), t + i * step, .9, g, -.2 + .1 * (i % 4), .4, .5)
# HOOK: record scratch-in, love sting, heartbeat
m.brass_hit([hz('D4'), hz('F#4'), hz('A4')], 0, .7, .25); m.crash(0, .3); m.sparkle(0.1, .8, .15)
romance(.4, ['A5', 'F#5', 'D5', 'E5', 'F#5'], .28, .14)
for i in range(4): m.pop(.5 + i * .3, .3, 700 + i * 150, -.4 + i * .27)
m.heartbeat(1.7, .5)
# PELÉ 1958/62/70: projector crackle + music box waltz; three dings; colour burst in 1970
t = 2.2; m.tape_rewind(t - .05, .3, .25); crackle(t, t + 4.4, .5)
m.music_box(t + .1, ['D5', 'F#5', 'A5', 'F#5', 'G5', 'B5', 'D6', 'B5', 'A5', 'F#5', 'E5', 'D5', 'E5', 'F#5', 'A5', 'D6'], .27, .12)
for b in (0.3, 1.9, 3.5): m.whoosh(t + b, .35, .2, True, .3); m.ding(t + b + .5, 1568 + b * 60, .3); m.f(m.wav('cheer_crowd'), t + b + .55, .12, 0, .3)
c = t + 4.4; m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4')], c, .9, .35); m.crash(c, .4); samba(c, 8.2, .8); m.cheer_burst(c + .1, .3)
# R9 1994: VHS hiss + clunk, bench whistle, polite clap, "0 minutes" sad tuba
t = 8.2; m.f(hp(noise(.08), 1000) * dec(.08, 30), t, .5); m.f(lp(hp(noise(3.0), 2000), 7000) * .2, t, .25)
m.drone(hz('D3'), t, 3.0, .06); m.tweet(t + .6, 3, .1)
for i in range(6): m.clap(t + .9 + i * .18, .12)
m.ding(t + 1.6, 1568, .25)
for i, (n, d) in enumerate([('F3', .25), ('E3', .25), ('D3', .5)]): tt = T(d); m.m(lp(osc(hz(n) * (1 + .02 * np.sin(2 * np.pi * 6 * tt)), d, 'saw'), 800) * env(len(tt), .02, .08), t + 1.8 + i * .26, .25, .2, .3)
# R9 2002: hair "boing", samba carnival, two goals, crowd
t = 11.2; m.boing(t + .1, .35); samba(t, 14.8, 1.0, 120)
for g in (0.5, 1.2): m.thwack(t + g - .3, .7); m.net(t + g, .5); m.cheer_burst(t + g + .05, .3); m.ding(t + g + .1, 1760 + g * 200, .25)
m.ding(t + 1.9, 2093, .3); m.f(m.wav('cheer_crowd'), t + 1.9, .3, 0, .3)
m.scratch(t + 2.35, .3); m.badumtss(t + 2.45, .45)
# MESSI 2022: desert night pad, cape whoosh, choir lift, fireworks
t = 14.8; m.choir([hz('D3'), hz('A3'), hz('F#4')], t, 1.0, .1); m.whoosh(t + .5, .4, .35, True)
m.drone(hz('D2'), t, 1.0, .08); m.heartbeat(t + .3, .4); m.heartbeat(t + .75, .45)
c = t + 1.0; m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4'), hz('A4')], c, 1.2, .4); m.crash(c, .5); m.choir([hz('D4'), hz('F#4'), hz('A4'), hz('D5')], c, 2.9, .12)
for i in range(6): m.firework(c + .2 + i * .45, .3, -.5 + i * .2)
m.cheer_burst(c + .1, .4); m.harp_gliss(c + .3, ['D5', 'E5', 'F#5', 'A5', 'B5', 'D6', 'E6'], .05, .12)
# CR7: walking footsteps, door creak, smooth "romantic" jazz, sparkle, shy squeak
t = 18.8
for i in range(5): m.footstep(t + i * .2, .25, .3)
cr = bp(osc(glide(220, 520, .6, .5), .6, 'saw'), 300, 2500) * (1 + .6 * np.sin(2 * np.pi * 23 * T(.6))) * env(int(.6 * SR), .02, .1)
m.f(cr, t + 1.2, .25, -.2, .2); m.boing(t + 1.5, .2, .4, 300, 200)
a = t + 2.2; m.sparkle(a, 1.2, .18); m.choir([hz('F#3'), hz('A3'), hz('C#4'), hz('E4')], a, 1.2, .08)
for i, n in enumerate(['F#3', 'B2', 'E3', 'A2', 'D3', 'G2']): m.bass(hz(n), a + i * .8, .7, .25)
for k in range(10): m.hat(a + k * .4, .06); m.rim(a + .4 + k * .8, .12) if k < 5 else None
romance(a + .2, ['A4', 'C#5', 'E5', 'G#5', 'F#5', 'E5', 'C#5', 'B4', 'A4', 'G#4', 'A4', 'B4', 'C#5', 'E5'], .32, .13)
m.pop(a + .9, .4, 1100); m.f(m.wav('chuckle'), a + 1.25, .35, -.3, .2)
m.boing(a + 1.6, .25, .3, 600, 900); m.f(m.wav('ooh_crowd'), a + 1.7, .35, 0, .3)
m.scratch(a + 2.35, .25); m.f(m.wav('laugh_crowd'), a + 2.5, .3, 0, .3)
# QUESTION + THANKS
t = 25.8; m.ding(t, 1318, .3); m.pop(t + .3, .3); m.pop(t + .45, .3); m.f(m.wav('ooh_crowd'), t + .2, .3, 0, .3); m.heartbeat(t + 1.0, .4); m.heartbeat(t + 1.6, .4)
t = 28.4
for i, n in enumerate(['D5', 'F#5', 'A5', 'D6', 'A5', 'F#5', 'D6']): m.pluck(hz(n), t + .1 + i * .16, .6, .22, -.3 + i * .1, .5, .4)
m.ding(t + 1.0, 2093, .35); m.pop(t + 1.0, .3)
m.write(sys.argv[1])
