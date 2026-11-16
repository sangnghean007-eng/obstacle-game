"""Ep14 CR7 ACADEMY sound: playful bounce music + slapstick. No TTS.
hook 0 · obsess 3.2 · door 8.6 · jump 12.0 · flip 16.6 · kick 21.2 · final 26.0 · goat 32.0 · tag 38.4 · end 42.4"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
# v2 timeline: a 1.6 s TV close-up is added first, and some segments are slowed (clarity pass). Remap every event from the v1 times.
OLD = [(0, 3.2, 1), (3.2, 5.4, 1.1), (8.6, 3.4, 1.2), (12.0, 4.6, 1.25), (16.6, 4.6, 1.2), (21.2, 4.8, 1.2), (26.0, 6.0, 1.1), (32.0, 6.4, 1), (38.4, 4.0, 1)]
NEW0 = []; _t = 1.6
for a, d, sl in OLD: NEW0.append(_t); _t += d * sl
def R(t):
    for (a, d, sl), n0 in zip(OLD, NEW0):
        if t < a + d or (a, d, sl) == OLD[-1]: return n0 + (t - a) * sl
END = _t; m = Mix(END)
_put = m.put; m.put = lambda bus, s, t0, *a, **k: _put(bus, s, R(t0), *a, **k)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def bounce(t0, t1, g=1.0, bpm=118, key='C'):
    b = 60 / bpm; t = t0; i = 0; root = {'C': 'C3', 'F': 'F2', 'G': 'G2'}[key]; prog = [0, 5, 7, 5]
    while t < t1 - .05:
        f = hz(root) * 2 ** (prog[(i // 4) % 4] / 12)
        m.bass(f, t, b * .45, .22 * g); m.bass(f * 1.5, t + b / 2, b * .4, .14 * g)
        if i % 2: m.snare(t, .14 * g)
        else: m.kick(t, .3 * g)
        m.pluck(f * 4 * [1, 1.25, 1.5, 2][i % 4], t + b / 4, .25, .07 * g, .3, .9, .3)
        t += b; i += 1
def slide(t, f0, f1, d=.5, g=.3): tt = T(d); m.f(osc(glide(f0, f1, d), d) * env(len(tt), .01, .05), t, g, 0, .15)
def slapfx(t, g=.8): m.whoosh(t - .2, .2, .22, True, .3); m.f(hp(noise(.07), 1800) * dec(.07, 55) * 1.6, t, g, 0, .08); m.f(osc(glide(220, 90, .12), .12) * dec(.12, 25), t, g * .7)
def whistle(t, d=.35, g=.3): tt = T(d); m.f(osc(2900 + 150 * np.sin(2 * np.pi * 40 * tt), d) * env(len(tt), .01, .05), t, g, .1, .1)
def knock(t): m.f(lp(noise(.08), 900) * dec(.08, 40) * 1.5 + osc(180, .08) * dec(.08, 30), t, .6, -.2, .1)
# HOOK: TV goal, jaw drop, mate falls, love harp
m.f(m.wav('cheer_crowd'), 0, .3, .3, .3); m.thwack(.15, .5, .4); m.net(.4, .4, .4); m.scratch(.6, .35); m.f(m.wav('gasp'), .65, .35, 0, .2)
m.whoosh(.7, .3, .2, False); m.f(bp(noise(.3), 400, 3000) * dec(.3, 9), 1.1, .35, .2); m.harp_gliss(1.25, ['C5', 'E5', 'G5', 'C6', 'E6', 'G6'], .06, .16); m.music_box(1.9, ['E5', 'G5', 'C6'], .25, .12)
# OBSESS: rewinds + counter dings, then backyard fail
t = 3.2; m.music_box(t, ['C5', 'E5', 'G5', 'E5', 'C5', 'E5', 'G5', 'C6'], .3, .1)
for k, tt_ in enumerate([.8, 1.6, 2.2]): m.tape_rewind(t + tt_ - .3, .3, .25); m.ding(t + tt_, 1568 + k * 200, .22)
t = 6.0; m.whoosh(t + .3, .4, .3, True); slide(t + .35, 400, 1400, .5, .2); m.thud(t + .9, .7); m.f(m.wav('chuckle'), t + 1.0, .25, -.3, .2); m.whoosh(t + 1.1, .3, .2, False); m.bonk(t + 1.5, .8); m.tweet(t + 1.6, 4, .14)
# DOOR: knocks, creak, puppy eyes, SIUUU
t = 8.6
for k in range(3): knock(t + .2 + k * .35); knock(t + .9 + k * .15)
cr = bp(osc(glide(220, 520, .6, .5), .6, 'saw'), 300, 2500) * (1 + .6 * np.sin(2 * np.pi * 23 * T(.6))) * env(int(.6 * SR), .02, .1); m.f(cr, t + 1.4, .25, .2, .2)
m.music_box(t + 1.6, ['A5', 'G5', 'E5', 'D5'], .2, .12); m.f(m.wav('siu'), t + 2.5, .8, .2, .25)
# ACADEMY music bed
bounce(12.0, 26.0, .8)
# JUMP: whistle, CR7 rocket jump, Messi 2 cm, SLAP
t = 12.0; whistle(t + .1); slide(t + .5, 300, 1600, .55, .25); m.thud(t + 1.6, .5); m.boing(t + 2.0, .25, .3, 300, 380); m.f(m.wav('ooh_crowd'), t + 2.4, .2, 0, .3); slapfx(t + 3.04); m.tweet(t + 3.15, 4, .12); m.f(m.wav('laugh_crowd'), t + 3.2, .25, 0, .3)
# FLIP: CR7 backflip, Messi drill-spin, THUNK, POP
t = 16.6; m.whoosh(t + .3, .6, .25, True); m.ding(t + 1.2, 1760, .2); slide(t + 1.6, 1500, 300, .9, .25); m.thud(t + 2.5, .7); m.f(bp(noise(.2), 200, 900) * dec(.2, 10), t + 2.5, .5)
for k in range(6): m.pop(t + 2.7 + k * .18, .15, 500 + k * 60)
m.f(m.wav('laugh_crowd'), t + 2.8, .25, 0, .3); m.pop(t + 3.8, .5, 700); m.boing(t + 3.85, .3, .4, 200, 600)
# KICK: CR7 perfect, SIUUU; Messi miss, BONK, facepalm, BOOT, into the net
t = 21.2; m.whoosh(t + .3, .4, .3, True); m.thwack(t + .6, .9); m.net(t + 1.2, .6); m.f(m.wav('siu'), t + 1.25, .7, 0, .25); m.cheer_burst(t + 1.25, .3)
m.whoosh(t + 2.3, .4, .25, True); m.f(m.wav('gasp'), t + 2.6, .25, 0, .2); m.bonk(t + 2.95, .8); m.f(osc(150, .1) * dec(.1, 30), t + 3.05, .5)
m.thwack(t + 3.45, 1.0); m.boing(t + 3.5, .35, .6, 200, 700); slide(t + 3.6, 600, 1800, .7, .2); m.net(t + 4.25, .7); m.tweet(t + 4.35, 4, .12); m.f(m.wav('laugh_crowd'), t + 4.3, .3, 0, .3)
# FINAL: drumroll, kick, BONK on CR7, steam, slipper fight
t = 26.0
for k in range(24): m.snare(t + .1 + k * .045, .08 + .25 * k / 24)
m.crash(t + 1.2, .3); m.thwack(t + 1.4, .8); m.whoosh(t + 1.6, .3, .3, True, .4); m.bonk(t + 2.0, 1.0); m.f(m.wav('ooh_crowd'), t + 2.05, .35, 0, .3)
m.f(hp(noise(.5), 2500) * env(int(.5 * SR), .05, .2), t + 2.2, .3); m.f(m.wav('grumble_angry'), t + 2.25, .4, .3, .2)
for k in range(15): slapfx(t + 2.85 + k * .2 + (k % 3) * .03, .55); m.pop(t + 2.95 + k * .2, .2, 600 + (k % 4) * 150, (-1) ** k * .4)
m.f(m.wav('laugh_crowd'), t + 3.4, .35, 0, .3); m.f(m.wav('wail'), t + 4.4, .3, -.3, .2)
# GOAT: sunset guitar, footsteps, sigh, SIUUU, bleat + crunch
t = 32.0; [m.pluck(hz(n), t + .1 + i * .32, .7, .13, -.2 + .05 * i, .5, .4) for i, n in enumerate(['G4', 'B4', 'D5', 'G5', 'F#5', 'D5', 'B4', 'G4', 'A4', 'C5', 'E5', 'G5', 'F#5', 'D5', 'B4', 'G4', 'A4', 'D5', 'G5'])]
for k in range(8): m.footstep(t + k * .2, .2, -.3)
m.f(m.wav('grumble_sad'), t + 1.8, .3, -.3, .2); m.f(m.wav('siu'), t + 2.6, .8, .2, .25); m.f(m.wav('bleat'), t + 3.3, .6, .1, .2)
for k in range(12): m.f(bp(noise(.05), 1500, 5000) * dec(.05, 50), t + 3.4 + k * .12, .25, .3)
m.f(m.wav('laugh_crowd'), t + 3.6, .3, 0, .3); m.f(m.wav('bleat'), t + 5.0, .4, .2, .2)
# TAG: sneaky pizzicato + sting
t = 38.4
for i, n in enumerate(['C4', 'E4', 'G4', 'C4', 'D#4', 'G4', 'C4', 'D4', 'F4']): m.pluck(hz(n), t + .1 + i * .22, .3, .14, -.2, .9, .2)
m.ding(t + 1.2, 1318, .3); m.brass_hit([hz('C3'), hz('G3'), hz('C4')], t + 1.25, .6, .25); m.pop(t + 1.8, .3, 900); m.f(m.wav('chuckle'), t + 2.3, .25, -.3, .2)
# v2: TV close-up sounds (placed directly, not remapped)
m.put = _put
m.f(m.wav('cheer_crowd'), 0, .35, 0, .3); m.whoosh(.15, .5, .3, True); m.thwack(.6, .9); m.whoosh(.62, .4, .3, True, .4); m.net(1.05, .7, .4); k808(1.05, 1.0); m.crash(1.05, .5); m.cheer_burst(1.05, .5)
m.write(sys.argv[1])
