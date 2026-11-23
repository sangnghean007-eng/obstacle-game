"""fx2: second-generation cartoon SFX + a variety guard. Every hit is re-synthesized with a fresh seed
(pitch, length, filter, layer mix), so repeated gags never play the identical waveform.
    from fx2 import Mix2;  m = Mix2(dur, ep=17)   # Mix + new sounds + m.vo(who, method, t, ...)
"""
import numpy as np
from synth import *
from vox2 import Voice, crowd


class Mix2(Mix):
    def __init__(self, dur, ep=0):
        super().__init__(dur); self.ep = ep; self.r = np.random.default_rng(1000 + ep); self._voices = {}; self._n = 0
    def v(self, who):
        if who not in self._voices: self._voices[who] = Voice(who, self.ep)
        return self._voices[who]
    def vo(self, who, what, t, g=.8, pan=0, *a, **k):  # character vocal on the voice bus
        x = getattr(self.v(who), what)(*a, **k); self.put(self.vox, x, t, g, pan, .08)
    def crowd(self, t, kind='laugh', d=2.0, g=.35, pan=0):
        self._n += 1; self.f(crowd(kind, d, seed=self.ep * 100 + self._n), t, g, pan, .25)
    def j(self, a=.9, b=1.1): return self.r.uniform(a, b)

    # ---------- new cartoon palette ----------
    def slide_whistle(self, t, up=True, d=.6, g=.3, pan=0):
        f0, f1 = (500 * self.j(), 1800 * self.j()) if up else (1800 * self.j(), 400 * self.j()); tt = T(d)
        self.f(osc(glide(f0, f1, d, .7) * (1 + .01 * np.sin(2 * np.pi * 6 * tt)), d) * env(len(tt), .03, .08) + .02 * noise(d), t, g, pan, .15)
    def kazoo(self, t, notes, step=.22, g=.18, pan=0):
        for i, n in enumerate(notes):
            if not n: continue
            d = step * .95; tt = T(d); x = osc(hz(n) * (1 + .015 * np.sin(2 * np.pi * 7 * tt)), d, 'saw'); x = bp(x, 400, 3500) * (1 + .4 * noise(d) * .3)
            self.m(x * env(len(tt), .02, .05), t + i * step, g, pan, .15)
    def squeak(self, t, g=.3, pan=0):
        d = .12 * self.j(); f = 1800 * self.j(.8, 1.3); self.f(osc(glide(f, f * 1.6, d), d, 'tri') * env(int(d * SR), .005, .04), t, g, pan)
    def timpani(self, t, f=90, g=.6, roll=0.0):
        if roll:
            for k in range(int(roll / .05)): d = .3; self.m(osc(f * self.j(.98, 1.02), d) * dec(d, 9) * (k / (roll / .05)) ** 1.5, t + k * .05, g * .3, 0, .3)
        d = 1.2; self.m((osc(np.concatenate([glide(f * 1.08, f, .1), np.full(int(1.1 * SR), f)])[:int(d * SR)], d) + .4 * osc(f * 1.5, d)) * dec(d, 3.5) + .15 * lp(noise(d), 400) * dec(d, 20), t + roll, g, 0, .3)
    def xylo(self, t, notes, step=.07, g=.2, pan=0):
        for i, n in enumerate(notes): d = .4; self.m((osc(hz(n), d) + .3 * osc(hz(n) * 3.9, d)) * dec(d, 14), t + i * step, g, pan, .2)
    def xylo_fall(self, t, g=.2): self.xylo(t, ['C6', 'A5', 'F5', 'D5', 'B4', 'G4', 'E4', 'C4'], .06, g)
    def xylo_rise(self, t, g=.2): self.xylo(t, ['C4', 'E4', 'G4', 'C5', 'E5', 'G5', 'C6'], .05, g)
    def cowbell(self, t, g=.25): d = .35; self.f((osc(587, d, 'sq') + osc(845, d, 'sq')) * .5 * dec(d, 12), t, g, .2)
    def tuba(self, t, n, d=.35, g=.3): tt = T(d); self.m(lp(osc(hz(n), d, 'saw'), 600) * env(len(tt), .03, .08), t, g, -.1, .15)
    def oompah(self, t0, t1, bass=('C2', 'G1'), bpm=120, g=.6):
        b = 60 / bpm; t = t0; i = 0
        while t < t1 - .02: self.tuba(t, bass[(i // 2) % len(bass)], b * .6, .3 * g) if i % 2 == 0 else self.organ_stab([hz('E4'), hz('G4'), hz('C5')], t, .12, .06 * g); t += b / 2; i += 1
    def whip(self, t, g=.5, pan=0): d = .25; self.f(hp(noise(d), 2500) * env(int(d * SR), .18, .02) * np.linspace(.2, 1, int(d * SR)), t, g, pan); self.f(hp(noise(.03), 1500) * dec(.03, 60), t + .23, g)
    def honk(self, t, g=.3): d = .3; self.f(bp(osc(330 * self.j(), d, 'saw') + osc(415 * self.j(), d, 'saw'), 300, 2000) * env(int(d * SR), .01, .05), t, g)
    def zip(self, t, g=.3, up=True): d = .2; self.f(bp(noise(d), 2000, 6000) * env(int(d * SR), .01, .05) * (1 + np.sin(2 * np.pi * 90 * T(d))), t, g)
    def cork(self, t, g=.4): self.pop(t, g, 500 * self.j()); self.f(osc(glide(700, 1400, .08), .08) * dec(.08, 20), t + .01, g * .5)
    def spring(self, t, g=.35, d=.7): tt = T(d); self.f(osc(220 * self.j() * (1 + .3 * np.sin(2 * np.pi * 14 * tt) * np.exp(-tt * 4)), d, 'tri') * dec(d, 4), t, g)
    def smack(self, t, g=.8, pan=0):  # varied slap / impact: body + crack layers re-mixed per call
        d = .12; body = lp(noise(d), 600 * self.j()) * dec(d, 25 * self.j()); crack = hp(noise(.03), 2500 * self.j()) * dec(.03, 70)
        self.f(body * self.j(.6, 1.0), t, g, pan); self.f(crack, t + .002, g * self.j(.5, .9), pan)
    def thump(self, t, g=.8): d = .35; self.f(osc(glide(120 * self.j(), 45, d, .4), d) * dec(d, 9) + .3 * lp(noise(d), 300) * dec(d, 30), t, g)
    def clang(self, t, g=.4, pan=0):
        d = 1.2; fs = [523 * self.j(), 1245 * self.j(), 1873 * self.j(), 2650 * self.j()]; self.f(sum(osc(f, d) * dec(d, 2 + i) for i, f in enumerate(fs)) * .3, t, g, pan, .3)
    def boom(self, t, g=.9): d = 1.4; self.f(lp(noise(d), 700) * dec(d, 3) + osc(glide(70, 30, d), d) * dec(d, 4), t, g, 0, .2); self.crash(t + .02, .35)
    def rain(self, t, d, g=.1): n = int(d * SR); x = hp(noise(d), 2500) * .5; drops = np.zeros(n); idx = self.r.integers(0, n, int(d * 40)); drops[idx] = self.r.uniform(.3, 1, len(idx)); self.f(x + lp(drops, 4000) * 2, t, g, 0, .2)
    # --- meme-style punctuation (synthesized here, no sampled meme audio; lesson from Remotion's sfx rule, 24 Nov 2026)
    def record_scratch(self, t, g=.5):  # vinyl stop: noisy pitch-dive + scratch
        d = .45; k = T(d); f = 900 * np.exp(-k * 7) + 80; x = bp(noise(d), 300, 3000) * (1 + np.sin(2 * np.pi * np.cumsum(f) / SR)) * dec(d, 5); self.f(x * g, t, 0)
    def sub_boom(self, t, g=.8):  # deep reverb boom for a reveal (vine-boom-like, own synth)
        d = 1.6; k = T(d); x = osc(glide(60 * self.j(), 32, d), d) * np.exp(-k * 2.2) + lp(noise(d), 180) * np.exp(-k * 6) * .6; self.f(x * g, t, 0, .3)
    def fail_horn(self, t, g=.3):  # descending trombone-style "wah wah wah waaah"
        for i, n in enumerate((392, 370, 349, 330)): d = .3 if i < 3 else .9; self.f(bp(osc(glide(n, n * (.94 if i == 3 else 1), d), d, 'saw'), 200, 2200) * env(int(d * SR), .03, .08) * (1 + .3 * np.sin(2 * np.pi * 6 * T(d)) * (i == 3)), t + i * .32, g)
    def wahwah(self, t, g=.22):  # muted-trumpet fail, randomized key
        k = self.r.integers(-3, 3)
        for i, n in enumerate([0, -1, -2, -3]): d = .35 if i < 3 else 1.0; tt = T(d); f = 330 * 2 ** ((n + k) / 12); o = osc(f, d, 'saw'); w = (np.sin(2 * np.pi * 4 * tt) > 0); x = bp(o, 300, 1300) * (1 - w) + bp(o, 300, 2800) * w; self.m(x * env(len(tt), .02, .1), t + i * .36, g, 0, .3)
