"""Ep28 THE DUEL sound: spaghetti-western parody (new style for the series): lonely whistle melody, twangy plucked guitar
(Karplus-Strong), whip cracks, wind + tumbleweed, a bell on every goal, Swedish crowd roars, train chug + whistle at the end."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('w0', 3.0), ('w1', 3.0), ('w2', 4.0), ('w3', 5.0), ('w4', 5.4), ('w5', 2.0), ('w6', 5.0), ('w7', 4.6), ('w8', 5.5), ('w9', 4.8)]
ST = {}; _t = 0
for n, d in SEGS: ST[n] = _t; _t += d
END = _t; m = Mix2(END, ep=28); at = lambda n, z: ST[n] + z
def pluck(f, d=1.2, g=.3, bright=.5):  # Karplus-Strong twang
    n = int(d * SR); L = max(2, int(SR / f)); buf = np.random.default_rng(int(f)).uniform(-1, 1, L); out = np.zeros(n)
    for i in range(n): out[i] = buf[i % L]; buf[i % L] = (buf[i % L] + buf[(i + 1) % L]) * (.5 - .002 * (1 - bright))
    return out * g
def twang(t, notes, step=.18, g=.28):
    for i, nn in enumerate(notes): m.m(pluck(hz(nn), 1.1, g), t + i * step, 1.0)
def whistle(t, notes, dur=.45, g=.16):  # lonely whistle with vibrato and slides
    for i, (nn, d) in enumerate(notes):
        n = int(d * SR); tt = np.arange(n) / SR; f = hz(nn) * (1 + .012 * np.sin(2 * np.pi * 5.5 * tt)) * np.minimum(1, .94 + tt * 1.2)
        m.m(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .05, .12) + .02 * noise(d), t, g); t += d
def wind(t, d, g=.12): n = int(d * SR); m.f(bp(noise(d), 300, 1200) * (0.6 + .4 * np.sin(np.arange(n) / SR * 2 * np.pi * .4)) * env(n, .5, .6), t, g)
def bell(t, g=.35):
    for f, a in ((660, 1), (1584, .5), (2350, .3)): m.f(osc(f, 1.6) * dec(1.6, 2.5) * a, t, g)
def chug(t0, t1, g=.25):
    t = t0
    while t < t1: m.f(lp(noise(.12), 900) * dec(.12, 25), t, g); t += .18
# OPEN: wind, tumbleweed, the whistle theme, whip
wind(0, 6.5, .14); m.whip(at('w0', .2), .5); whistle(at('w0', .4), [('A5', .5), ('D6', .5), ('A5', .35), ('D6', .35), ('A5', 1.2)])
twang(at('w0', 1.0), ['D3', 'A3', 'D4'], .25); m.f(lp(noise(2.4), 600) * env(int(2.4 * SR), .3, .4), at('w0', .3), .08)
# STAKES: ball spin on the finger, neck crack x2, slow strummed bass
for i in range(8): m.f(hp(noise(.03), 3000) * dec(.03, 60), at('w1', .3 + i * .12), .12)
for k in (1.65, 2.05): m.f(hp(noise(.05), 1500) * dec(.05, 40), at('w1', k), .55); m.vo('generic_m', 'grunt', at('w1', k + .02), .3)
twang(at('w1', .2), ['D3', 'F3', 'A3', 'C4', 'A3'], .5, .22)
# 50' Ronaldo: tension pluck, the shot (whip + whoosh), net, bell, crowd groan
twang(at('w2', .1), ['D3', 'D3', 'D3'], .3, .2); m.whip(at('w2', 1.0), .7); m.whoosh(at('w2', 1.02), .35, .4, True); m.thump(at('w2', 1.4), .6); bell(at('w2', 1.42))
m.crowd(at('w2', 1.6), 'gasp', 1.0, .3); m.vo('ronaldo', 'laugh', at('w2', 1.9), .4, -.3, 'snicker'); whistle(at('w2', 2.3), [('D6', .3), ('F6', .3), ('A5', .8)], g=.12)
# 68' Zlatan header: corner whistle, crowd rising, BONK, Ronaldo spins, bell, roar
m.f(lp(osc(2900, .35, 'sq'), 5000) * (1 + .5 * np.sign(np.sin(np.arange(int(.35 * SR)) / SR * 2 * np.pi * 30))) * env(int(.35 * SR), .01, .05), at('w3', .1), .08); m.crowd(at('w3', .6), 'cheer', 1.0, .18); m.vo('haaland', 'grunt', at('w3', 1.55), .6); m.bonk(at('w3', 1.6), .8); m.whoosh(at('w3', 1.65), .45, .4)
m.spring(at('w3', 1.8), .35); m.thump(at('w3', 2.1), .6); bell(at('w3', 2.12)); m.crowd(at('w3', 2.2), 'cheer', 2.2, .55); m.vo('ronaldo', 'yelp', at('w3', 1.9), .45)
twang(at('w3', 2.6), ['A3', 'C4', 'D4', 'F4'], .15, .2)
# 72' free kick: drum roll, low zip through the wall, bell, roar, smoke blow, "I AM ZLATAN" sting
m.timpani(at('w4', 0), 70, .35, roll=.8); m.vo('generic_m', 'yelp', at('w4', 1.05), .35); m.zip(at('w4', 1.0), .4); m.thump(at('w4', 1.35), .6); bell(at('w4', 1.37)); m.crowd(at('w4', 1.4), 'cheer', 2.6, .6)
m.f(lp(noise(.5), 1200) * env(int(.5 * SR), .05, .3), at('w4', 1.6), .2)
for i in range(4): m.footstep(at('w4', 2.2 + i * .25), .35)
m.cork(at('w4', 2.7), .3); m.brass_hit([hz('D3'), hz('A3'), hz('D4')], at('w4', 3.4), .8, .25); m.vo('ronaldo', 'gasp', at('w4', 3.45), .45)
# HOLD: heartbeat + sweat drops
for i in range(3):
    m.thump(at('w5', .1 + i * .6), .35); m.f(osc(glide(1200, 600, .08), .08) * dec(.08, 30), at('w5', .4 + i * .6), .1)
# 77': shirt rip, abs shine, kick, PING off the ticket, bell
m.f(hp(noise(.35), 1500) * env(int(.35 * SR), .01, .1), at('w6', .4), .55); m.vo('ronaldo', 'grunt', at('w6', .42), .55); m.sparkle(at('w6', .9), .7, .25); twang(at('w6', 1.0), ['D4', 'F4', 'A4', 'D5'], .12, .22)
m.whip(at('w6', 2.0), .7); m.whoosh(at('w6', 2.02), .3, .4, True); m.f(osc(2600, .3) * dec(.3, 12), at('w6', 2.3), .3); m.vo('generic_m', 'gasp', at('w6', 2.32), .4); m.thump(at('w6', 2.6), .6); bell(at('w6', 2.62)); m.crowd(at('w6', 2.7), 'gasp', 1.2, .3)
# 79': counter run, hat-trick, POP the man-bun, SIUUU, whistle theme triumphant
for i in range(5): m.footstep(at('w7', .7 + i * .16), .4)
m.whip(at('w7', 1.5), .7); m.thump(at('w7', 1.9), .7); bell(at('w7', 1.92)); bell(at('w7', 2.1), .25); m.cork(at('w7', 1.95), .45); m.vo('ronaldo', 'siu', at('w7', 2.3), .8); m.boom(at('w7', 2.35), .5)
whistle(at('w7', 3.0), [('D6', .3), ('A6', .3), ('D7', .9)], g=.13); twang(at('w7', 3.0), ['D3', 'A3', 'D4', 'F#4', 'A4'], .1, .24)
# TRAIN: chug in, whistle, footsteps, the quote (Zlatan hmph)
chug(at('w8', 0), at('w8', 1.1), .3); m.f(osc(glide(700, 760, .8), .8) * env(int(.8 * SR), .05, .2) + .5 * osc(glide(880, 950, .8), .8) * env(int(.8 * SR), .05, .2), at('w8', .9), .2)
m.f(lp(noise(.8), 1500) * dec(.8, 3), at('w8', 1.0), .25)
for i in range(5): m.footstep(at('w8', 1.25 + i * .22), .3)
m.vo('haaland', 'hmph', at('w8', 2.5), .55); twang(at('w8', 2.6), ['A3', 'G3', 'F3', 'E3'], .4, .2)
# SMOKE: whistle, chug away, PFFF of smoke, blink, sad trombone-ish whistle, wind
m.f(osc(glide(700, 760, .6), .6) * env(int(.6 * SR), .05, .2), at('w9', .1), .2); chug(at('w9', 0), at('w9', 2.4), .22); m.f(lp(noise(1.2), 500) * env(int(1.2 * SR), .1, .6), at('w9', .3), .45); m.vo('haaland', 'oof', at('w9', 1.0), .5)
m.f(osc(1800, .05) * dec(.05, 40), at('w9', 2.05), .2); m.wahwah(at('w9', 2.3), .2); wind(at('w9', 2.0), 2.8, .12); whistle(at('w9', 2.6), [('A5', .4), ('D5', 1.6)], g=.1)
# continuous western bed (QA: no dead air): boom-chick bass + muted strum + low drone, quieter under the gags
def bed(t0, t1, g=.5, bpm=92):
    b = 60 / bpm; t = t0; i = 0; roots = ['D2', 'A1', 'D2', 'C2', 'D2', 'A1', 'F2', 'A1']
    while t < t1 - .05:
        if i % 2 == 0: m.m(pluck(hz(roots[(i // 2) % 8]), .5, .5 * g), t, 1.0)
        else: m.m(hp(noise(.07), 1800) * dec(.07, 40) * .3 * g, t, 1.0)
        t += b / 2; i += 1
    n = int((t1 - t0) * SR); m.m(lp(osc(hz('D2'), t1 - t0, 'saw'), 300) * env(n, 1.0, 1.5) * .06 * g, t0, 1.0)
bed(0.3, END - 0.2, .55)
print(round(END, 2)); m.write(sys.argv[1])
