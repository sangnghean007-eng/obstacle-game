"""Ep4 v3 "IMMOVABLE" sound: no TTS. Tuba march, crowd, synthesized grunts/hum/yawn and strong foley. All synthesized."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *



S = dict(hook=0, setup=2.0, note=5.2, sneak=8.0, talk=12.8, fulltime=16.4, phone=19.4, thanks=22.4)
END = 25.0
m = Mix(END)


def tuba(f, t, d, g=.3): x = osc(f, d, 'saw') + .6 * osc(f, d, 'sq'); m.m(lp(x, 520) * env(len(x), .02, .08), t, g, 0, .12)
def march(t0, t1, g=1.0, bpm=112):
    b = 60 / bpm; line = ['D2', 'A1', 'D2', 'A1', 'F2', 'C2', 'F2', 'A1']; t = t0; i = 0
    while t < t1 - .05:
        tuba(hz(line[i % 8]), t, b * .8, .34 * g)
        (m.kick(t, .7 * g) if i % 2 == 0 else m.snare(t, .3 * g)); m.hat(t + b / 2, .07 * g)
        if i % 4 == 2: m.pluck(hz(['A4', 'D5', 'F5', 'E5'][(i // 4) % 4]), t, .3, .12 * g, .3)
        t += b; i += 1
def voice(t, d, f0, f1, g=.4, pan=0, lo=500, hi=1600, buzz=1.0):  # grunts made from a buzzy source through a mouth-like band
    tt = T(d); f = glide(f0, f1, d) * (1 + .03 * np.sin(2 * np.pi * 7 * tt)); x = osc(f, d, 'saw') * buzz + .3 * osc(f * 2, d)
    y = bp(x, lo, hi) + .4 * bp(x, hi * 1.6, hi * 2.2); y *= env(len(y), .03, .1) * (1 + .3 * np.sin(2 * np.pi * 11 * tt)); m.put(m.vox, y, t, g, pan, .03)
def hm(t, g=.5): d = .38; tt = T(d); x = osc(glide(115, 165, d, 2), d) + .25 * osc(glide(230, 330, d, 2), d); m.put(m.vox, lp(x, 600) * env(len(x), .03, .12), t, g, .2, .02)
def yawn(t, g=.4): voice(t, 1.0, 260, 120, g, .2, 350, 1100, .7)
def engine(t, d, g=.3):
    tt = T(d); f = 45 + 25 * tt / d; x = osc(f, d, 'saw') * (.6 + .4 * np.sign(np.sin(2 * np.pi * 14 * tt))); m.f(lp(x, 500) * env(len(x), .1, .05) * (.4 + .6 * tt / d), t, g, -.4, .05)
def metal(t, g=.5):
    m.f(bp(noise(.6), 800, 6000) * dec(.6, 7), t, g, 0, .4)
    for f in (523, 811, 1307, 1999): d = 1.0; m.f(osc(f, d) * dec(d, 5), t + .01, g * .25, np.random.uniform(-.5, .5), .4)
def rise(t, d=.7, g=.3): m.f(osc(glide(400, 2600, d, .6), d) * env(int(d * SR), .01, .1), t, g, -.4, .2)
def whistle_tune(t, g=.18):
    for i, n in enumerate(['G6', 'B6', 'D7', 'B6', 'A6', 'G6', None, 'D7', 'C7']):
        if n: d = .2; tt = T(d); m.f(osc(hz(n) * (1 + .01 * np.sin(2 * np.pi * 6 * tt)), d) * env(int(d * SR), .02, .05), t + i * .2, g, .3, .3)


def sq(f, t, d, g=.12, pan=0): x = osc(f, d, 'sq'); m.f(lp(x, 3000) * env(len(x), .005, .04), t, g, pan, .1)
def level_start(t): [sq(hz(n), t + i * .09, .12, .12) for i, n in enumerate(['C5', 'E5', 'G5', 'C6'])]
def heart_lost(t): [sq(hz(n), t + i * .09, .14, .14) for i, n in enumerate(['E5', 'C5', 'G4'])]; m.pop(t, .25, 400)
def game_over(t): [sq(hz(n), t + i * .2, .26, .16) for i, n in enumerate(['G4', 'F4', 'E4', 'D4', 'C4'])]
def giggle(t, n=6): [voice(t + i * .13, .1, 420 - i * 8, 380 - i * 8, .3, -.3, 700, 2200) for i in range(n)]
def pins(t): [m.f(bp(noise(.08), 1500, 5000) * dec(.08, 40) + osc(900 + 300 * (i % 3), .08) * dec(.08, 50) * .4, t + i * .045, .35, np.random.uniform(-.7, .7), .3) for i in range(12)]


def spy(t0, t1, bpm=100, g=1.0):  # original sneaky pizzicato theme (E minor)
    b = 60 / bpm; line = ['E2', 'G2', 'A2', 'B2', 'E2', 'G2', 'A#2', 'B2']; t = t0; i = 0
    while t < t1 - .05:
        m.pluck(hz(line[i % 8]), t, .2, .3 * g, -.1, .2, .05)
        if i % 2: m.hat(t, .09 * g, False, .3); m.f(bp(noise(.05), 1500, 4000) * dec(.05, 60), t, .12 * g, -.3, .2)   # brush + snap
        if i % 8 == 7: m.pluck(hz('B4'), t, .3, .12 * g, .4, .8, .3)
        t += b / 2; i += 1
def crinkle(t, d=.4): [m.f(bp(noise(.03), 2000, 8000) * dec(.03, 80), t + k * d / 10, .2, .2, .05) for k in range(10)]
def whir(t, d=.5, f0=300, f1=1400, g=.2): m.f(osc(glide(f0, f1, d), d, 'saw') * .3 * env(int(d * SR), .02, .05), t, g, .3, .1)
def reel(t, d=.5): [m.tick(t + k * .03, k % 2 == 0, .12) for k in range(int(d / .03))]
def sad_trombone(t):
    for i, (f0, d) in enumerate([(hz('D3'), .35), (hz('C#3'), .35), (hz('C3'), .35), (hz('B2'), .9)]):
        tt = T(d); f = f0 * (1 + .015 * np.sin(2 * np.pi * 6 * tt)) * (np.linspace(1, .97, len(tt)) if i == 3 else 1); x = lp(osc(f, d, 'saw'), 900) * env(len(tt), .03, .1)
        m.m(x, t + i * .4, .3, 0, .3)
def success(t): [sq(hz(n), t + i * .1, .16, .14) for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'E6'])]
def ref_whistle(t, n=3):
    for k in range(n): d = .25 if k < n - 1 else .6; tt = T(d); x = osc(2900 + 120 * np.sign(np.sin(2 * np.pi * 28 * tt)), d) + .3 * bp(noise(d), 2500, 4000); m.f(x * env(len(x), .01, .05), t + k * .32, .3, .2, .15)


def spy(t0, t1, bpm=100, g=1.0):  # original sneaky pizzicato theme (E minor)
    b = 60 / bpm; line = ['E2', 'G2', 'A2', 'B2', 'E2', 'G2', 'A#2', 'B2']; t = t0; i = 0
    while t < t1 - .05:
        m.pluck(hz(line[i % 8]), t, .2, .3 * g, -.1, .2, .05)
        if i % 2: m.hat(t, .09 * g, False, .3); m.f(bp(noise(.05), 1500, 4000) * dec(.05, 60), t, .12 * g, -.3, .2)   # brush + snap
        if i % 8 == 7: m.pluck(hz('B4'), t, .3, .12 * g, .4, .8, .3)
        t += b / 2; i += 1
def crinkle(t, d=.4): [m.f(bp(noise(.03), 2000, 8000) * dec(.03, 80), t + k * d / 10, .2, .2, .05) for k in range(10)]
def whir(t, d=.5, f0=300, f1=1400, g=.2): m.f(osc(glide(f0, f1, d), d, 'saw') * .3 * env(int(d * SR), .02, .05), t, g, .3, .1)
def reel(t, d=.5): [m.tick(t + k * .03, k % 2 == 0, .12) for k in range(int(d / .03))]
def sad_trombone(t):
    for i, (f0, d) in enumerate([(hz('D3'), .35), (hz('C#3'), .35), (hz('C3'), .35), (hz('B2'), .9)]):
        tt = T(d); f = f0 * (1 + .015 * np.sin(2 * np.pi * 6 * tt)) * (np.linspace(1, .97, len(tt)) if i == 3 else 1); x = lp(osc(f, d, 'saw'), 900) * env(len(tt), .03, .1)
        m.m(x, t + i * .4, .3, 0, .3)
def success(t): [sq(hz(n), t + i * .1, .16, .14) for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'E6'])]
def ref_whistle(t, n=3):
    for k in range(n): d = .25 if k < n - 1 else .6; tt = T(d); x = osc(2900 + 120 * np.sign(np.sin(2 * np.pi * 28 * tt)), d) + .3 * bp(noise(d), 2500, 4000); m.f(x * env(len(x), .01, .05), t + k * .32, .3, .2, .15)


def mumble(t, n, f0, g=.3, pan=0):  # cartoon "talk" blips (no words, no TTS)
    R = np.random.default_rng(int(t * 100))
    for i in range(n): f = f0 * (1 + R.uniform(-.25, .3)); d = .07 + R.random() * .04; x = bp(osc(f, d, 'saw'), 500, 2500) * env(int(d * SR), .005, .03); m.put(m.vox, x, t + i * .1, g, pan, .02)
def rain(t, d, g=.18): x = hp(noise(d), 3000) * (.6 + .4 * np.random.default_rng(1).random(int(d * SR))); m.f(lp(x, 9000) * env(len(x), .3, .4), t, g, -.2, .1)
def notif2(t): m.ding(t, 1568, .25, .3); m.ding(t + .09, 2093, .2, .3)

m.crowd(0, S['thanks'], .2, swell=False)
# HOOK
spy(0, 1.0, 96, .8)
for k in range(4): m.f(osc(hz('E6'), .08) * dec(.08, 40), .1 + k * .2, .12, .4, .1)
m.scratch(1.0, .45); m.boing(1.02, .35, .3, 400, 200); whistle_tune(1.15, .16)
# SETUP: two early goals, one back
t = S['setup']; m.ding(t + .1, 1760, .15)
for g in (.6, 1.3): m.cheer_burst(t + g, .4); m.kick(t + g, .9); m.crash(t + g, .3); m.brass_hit([hz('C3'), hz('G3'), hz('C4')], t + g, .4, .18)
m.f(m.wav('grumble_angry'), t + 1.6, .0)
voice(t + 1.5, .5, 160, 230, .35, -.3); m.kettle(t + 1.4, .7, .14)
m.cheer_burst(t + 2.3, .25); m.pop(t + 2.3, .3, 700)
# NOTE: paper plane, eyes zoom, spy theme starts
t = S['note']; m.whoosh(t, 1.0, .25, True, -.5); m.pop(t + 1.0, .3, 900); crinkle(t + 1.05, .3)
m.f(lp(osc(glide(100, 900, .5, 2), .5, 'saw'), 2000) * env(int(.5 * SR), .05, .05), t + 1.45, .25, 0, .3)   # zoom swoosh
m.brass_hit([hz('E3'), hz('B3'), hz('E4')], t + 1.7, .7, .25); m.crash(t + 1.7, .25)
spy(t + 1.7, S['sneak'], 100, .9)
# SNEAK
t = S['sneak']; spy(t, S['talk'], 108)
for k in range(16): m.footstep(t + k * .14, .18, -.4 + k * .04)
for k in range(5): m.f(osc(hz('E6') * (1 + k * .06), .08) * dec(.08, 40), t + 2.3 + k * .15, .14, .3, .1)
m.ding(t + 3.4, 2637, .25); m.sparkle(t + 3.45, .4, .12); m.brass_hit([hz('C4'), hz('E4'), hz('G4')], t + 3.4, .4, .18)
# TALK
t = S['talk']; mumble(t + .25, 9, 520, .32, -.3); m.pop(t + 1.2, .2, 900)
mumble(t + 1.65, 6, 260, .38, .3); m.boing(t + 2.4, .2, .3, 300, 150)
m.f(m.wav('ooh_crowd'), t + 2.3, .3, 0, .3)
# FULL TIME
t = S['fulltime']; ref_whistle(t + .15, 3); m.brass_hit([hz('C2'), hz('F#2'), hz('C3')], t + .3, .6, .25)
rain(t + .8, 2.2, .2); m.thud(t + .9, .4); sad_trombone(t + 1.0)
m.cheer_burst(t + .5, .25)
# PHONE
t = S['phone']; notif2(t + .2); notif2(t + 1.0); m.f(m.wav('laugh_crowd'), t + .35, .35, 0, .3)
m.whoosh(t + 2.2, .4, .3, False, -.3); m.thud(t + 2.5, .8); m.boing(t + 2.55, .3, .35, 260, 130); m.tweet(t + 2.65, 3, .13, -.4)
# THANKS
t = S['thanks']
for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'G5', 'E5', 'C6']): m.pluck(hz(n), t + .1 + i * .18, .6, .2, -.3 + i * .1, .5, .4)
m.saw_chord([hz('C4'), hz('E4'), hz('G4')], t + .1, 2.4, .05, 1600, 0, .3, .8, .4)
m.ding(t + 1.2, 2093, .35); m.pop(t + 1.2, .3); m.sparkle(t + 1.25, .5, .12); m.f(m.wav('cheer_crowd'), t + .2, .25, 0, .3)
m.write(sys.argv[1])
