"""Ep4 v3 "IMMOVABLE" sound: no TTS. Tuba march, crowd, synthesized grunts/hum/yawn and strong foley. All synthesized."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *




S = dict(arrive=0, ball=3.0, ice=7.0, stroller=11.2, messi=15.6, galaxy=18.6, reveal=22.0, thanks=25.0)
END = 27.6
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


def dembow(t0, t1, bpm=96, g=1.0):  # original Miami summer groove (A minor)
    b = 60 / bpm; t = t0; i = 0; mel = ['A4', 'C5', 'E5', 'D5', 'C5', 'E5', 'G5', 'E5']; bass = ['A1', 'A1', 'F1', 'G1']
    while t < t1 - .05:
        m.kick(t, .7 * g); m.snare(t + b * .75, .25 * g, .2); m.snare(t + b * 1.5, .3 * g, -.2); m.kick(t + b * 2, .6 * g); m.snare(t + b * 2.75, .25 * g, .2); m.snare(t + b * 3.5, .3 * g, -.2)
        for k in range(8): m.hat(t + k * b / 2, .07 * g, k % 2 == 1)
        m.bass(hz(bass[i % 4]), t, b * 1.5, .4 * g); m.bass(hz(bass[i % 4]) * 1.5, t + b * 2.5, b, .3 * g)
        for k in range(4): m.pluck(hz(mel[(i * 4 + k) % 8]), t + k * b, .3, .14 * g, .3, .9, .2)
        t += 4 * b; i += 1
def tear(t, g=.5): d = .35; x = bp(noise(d), 1500, 7000) * (1 + .8 * np.sign(np.sin(2 * np.pi * 70 * T(d)))) * env(int(d * SR), .005, .1); m.f(x, t, g, .1, .1)
def squawk(t, g=.25): d = .3; f = glide(1400, 900, d); x = osc(f, d, 'saw') * .5 + osc(f * 1.5, d); m.f(bp(x, 700, 3000) * env(int(d * SR), .02, .1), t, g, .4, .2)
def ref_tweet(t, g=.3): d = .4; tt = T(d); x = osc(2900 + 120 * np.sign(np.sin(2 * np.pi * 28 * tt)), d) + .3 * bp(noise(d), 2500, 4000); m.f(x * env(len(x), .01, .05), t, g, .3, .15)
def siren(t, d=1.6, g=.22): tt = T(d); f = np.where(np.sin(2 * np.pi * 1.6 * tt) > 0, 960, 770); m.f(osc(f, d, 'sq') * .4 * env(int(d * SR), .05, .2), t, g, -.4, .2)
def giggle_baby(t): [voice(t + i * .11, .09, 700 - i * 10, 640 - i * 10, .25, .3, 900, 2600) for i in range(6)]
def mumble(t, n, f0, g=.3, pan=0):
    R = np.random.default_rng(int(t * 100))
    for i in range(n): f = f0 * (1 + R.uniform(-.25, .3)); d = .07 + R.random() * .04; x = bp(osc(f, d, 'saw'), 500, 2500) * env(int(d * SR), .005, .03); m.put(m.vox, x, t + i * .1, g, pan, .02)

m.crowd(0, S['thanks'], .08, swell=False)   # light beach crowd
m.f(lp(noise(END), 700) * .25, 0, .25, 0, 0)  # waves
dembow(0, S['reveal'] - .1, 96, .85)
# ARRIVE
m.seagull(.3, .12); for_steps = [m.footstep(k * .2, .2, -.5 + k * .1) for k in range(7)]
whistle_tune(1.7, .14)
# BALL -> rip (United)
t = S['ball'] + 1.0
m.whoosh(t - .3, .3, .25, True, -.3); m.thud(t, .7); tear(t + .1, .6); m.boing(t + .1, .35, .4, 300, 600)
squawk(t + 1.0); ref_tweet(t + 1.25); m.ding(t + 1.4, 2093, .2)
# ICE CREAM -> rip (Madrid) -> guards 5 cups
t = S['ice']; m.music_box(t + .1, ['E5', 'G5', 'C6', 'G5', 'E5'], .16, .12)
t0 = t + 1.0; m.thud(t0, .7); tear(t0 + .1, .6); m.crash(t0, .25)
for k in range(4): m.pop(t0 + .15 + k * .1, .25, 900 + 200 * k)
squawk(t0 + 1.0); ref_tweet(t0 + 1.2); m.brass_hit([hz('C4'), hz('E4'), hz('G4')], t + 2.65, .5, .18)
# STROLLER -> heroic save -> rip x2
t = S['stroller']; m.f(osc(glide(500, 700, 1.0), 1.0) * .2 * env(int(SR), .1, .1), t, .15, .4, .1)
m.thud(t + .9, .6); m.brass_hit([hz('G3'), hz('C4'), hz('E4'), hz('G4')], t + 1.0, .6, .22); tear(t + 1.0, .5)
giggle_baby(t + 1.6); squawk(t + 1.7); m.ding(t + 2.2, 2637, .25)
tear(t + 2.95, .55); m.boing(t + 2.95, .3, .35, 260, 520)
# MESSI slip
t = S['messi']; m.footstep(t, .2); m.footstep(t + .3, .2)
mumble(t + 1.0, 5, 420, .34, .3); voice(t + 1.75, .25, 380, 520, .35, .3)   # gasp
m.f(m.wav('ooh_crowd'), t + 1.8, .25, 0, .3)
# GALAXY + probe
t = S['galaxy']
for k in range(6): m.footstep(t + k * .1, .25, .5)
mumble(t + .6, 7, 300, .36, .4); siren(t + 1.8, 1.8, .25); m.brass_hit([hz('C2'), hz('F#2'), hz('C3')], t + 2.2, .7, .25)
# REVEAL
t = S['reveal']; m.whoosh(t + .3, .5, .3, False); m.pop(t + .5, .3, 500); tear(t + .9, .55)
m.kick(t + 1.0, 1.0); m.crash(t + 1.0, .45); m.brass_hit([hz('A3'), hz('C#4'), hz('E4'), hz('A4')], t + 1.0, 1.2, .3); m.cheer_burst(t + 1.05, .45)
dembow(t + 1.2, S['thanks'], 104, .9)
# THANKS
t = S['thanks']
for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'G5', 'E5', 'C6']): m.pluck(hz(n), t + .1 + i * .18, .6, .2, -.3 + i * .1, .5, .4)
m.saw_chord([hz('C4'), hz('E4'), hz('G4')], t + .1, 2.4, .05, 1600, 0, .3, .8, .4)
m.ding(t + 1.2, 2093, .35); m.pop(t + 1.2, .3); m.sparkle(t + 1.25, .5, .12)
m.write(sys.argv[1])
